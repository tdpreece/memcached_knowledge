import socket
from time import sleep

import memcache


'''
http://balodeamit.blogspot.co.uk/2014/02/slab-reallocation-in-memcache.html
To do
- show getting into bad state and automove helping
  Add details to readme

memory allocated to memcached is 64MB (from /etc/memcached.conf), which
is equivalent to 64 pages.

The 500MB value will go in slab 40, which stores chunks of size up
to 616944KB and can store 1 chunk per page.
64 sets with unique keys will fill up the cache.
The 100MB value will go in slab 32, which stores chunks of size up
to 103496KB and can store 10 chunk per page.
640 sets with unique keys will fill up the cache.


'''


class MyClient(memcache.Client):
    def get_item_stats(self):
        data = []
        for s in self.servers:
            if not s.connect():
                continue
            if s.family == socket.AF_INET:
                name = '%s:%s (%s)' % (s.ip, s.port, s.weight)
            elif s.family == socket.AF_INET6:
                name = '[%s]:%s (%s)' % (s.ip, s.port, s.weight)
            else:
                name = 'unix:%s (%s)' % (s.address, s.weight)
            serverData = {}
            data.append((name, serverData))
            s.send_cmd('stats items')
            readline = s.readline
            while 1:
                line = readline()
                if not line or line.strip() == 'END':
                    break

                # e.g. STAT items:40:evicted_unfetched 1842
                item = line.split(' ', 2)
                slab = item[1].split(':', 2)[1:]
                if slab[0] not in serverData:
                    serverData[slab[0]] = {}
                serverData[slab[0]][slab[1]] = item[2]
        return data

    def get_my_stats(self):
        slab_stats_wanted = ('total_pages',)
        item_stats_wanted = ('evicted',)
        slab_stats = {
            k: v for k, v in
            self.get_slab_stats()[0][1].items() if k.isdigit()
        }
        item_stats = {
            k: v for k, v in
            self.get_item_stats()[0][1].items() if k.isdigit()
        }

        my_stats = {}
        for slab in slab_stats.keys():
            my_stats[slab] = {}
            for stat in slab_stats_wanted:
                my_stats[slab][stat] = slab_stats[slab][stat]
            for stat in item_stats_wanted:
                my_stats[slab][stat] = item_stats[slab][stat]
        return my_stats

    def enable_automove(self):
        for s in self.servers:
            if not s.connect():
                continue
            if s.family == socket.AF_INET:
                name = '%s:%s (%s)' % (s.ip, s.port, s.weight)
            elif s.family == socket.AF_INET6:
                name = '[%s]:%s (%s)' % (s.ip, s.port, s.weight)
            else:
                name = 'unix:%s (%s)' % (s.address, s.weight)
            s.send_cmd('slabs automove 1')
            s.expect(b'OK')

    def disable_automove(self):
        for s in self.servers:
            if not s.connect():
                continue
            if s.family == socket.AF_INET:
                name = '%s:%s (%s)' % (s.ip, s.port, s.weight)
            elif s.family == socket.AF_INET6:
                name = '[%s]:%s (%s)' % (s.ip, s.port, s.weight)
            else:
                name = 'unix:%s (%s)' % (s.address, s.weight)
            s.send_cmd('slabs automove 0')
            s.expect(b'OK')


def main():
    mc = MyClient(['127.0.0.1:11211'])
    mc.disable_automove()
    print(mc.get_my_stats())

    five_hundred_KB_value = 'b' * 500000
    for i in range(0, 150):
        mc.set('big-{}'.format(i), five_hundred_KB_value)

    print(mc.get_my_stats())

    one_hundred_KB_value = 'a' * 100000
    for i in range(0, 20):
        for i in range(0, 252):
            mc.set('small-{}'.format(i), one_hundred_KB_value)
        print(mc.get_my_stats())
        sleep(5)

    mc.enable_automove()
    print('Enabled automove')
    for i in range(0, 20):
        for i in range(0, 252):
            mc.set('small-{}'.format(i), one_hundred_KB_value)
        print(mc.get_my_stats())
        sleep(5)


if __name__ == '__main__':
    main()
