import socket

import memcache


'''
http://balodeamit.blogspot.co.uk/2014/02/slab-reallocation-in-memcache.html
To do
done - fill up the cache with items of two sizes with automove=false.
- print evictions from item stats
- show in bad state that cannot recover from
- show how automove may help

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


def main():
    mc = MyClient(['127.0.0.1:11211'])
    print_page_distribution(mc)

    five_hundred_KB_value = 'b' * 500000
    for i in range(0, 150):
        mc.set('big-{}'.format(i), five_hundred_KB_value)

    print_page_distribution(mc)

    one_hundred_KB_value = 'a' * 100000
    for i in range(0, 252):
        mc.set('small-{}'.format(i), one_hundred_KB_value)
    print_page_distribution(mc)
    print_numbers_evicted(mc)


def print_page_distribution(memcache_client):
    slab_stats = {
        k: v for k, v in
        memcache_client.get_slab_stats()[0][1].items() if k.isdigit()
    }
    page_distribution = [
        (slab, stats['total_pages']) for slab, stats in slab_stats.items()
    ]
    print(page_distribution)


def print_numbers_evicted(memcache_client):
    item_stats = {
        k: v for k, v in
        memcache_client.get_item_stats()[0][1].items() if k.isdigit()
    }
    numbers_evicted = [
        (slab, stats['evicted']) for slab, stats in item_stats.items()
    ]
    print(numbers_evicted)


if __name__ == '__main__':
    main()
