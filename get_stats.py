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

def main():
    mc = memcache.Client(['127.0.0.1:11211'])
    print_page_distribution(mc)

    five_hundred_KB_value = 'b' * 500000
    for i in range(0, 150):
        mc.set('big-{}'.format(i), five_hundred_KB_value)

    print_page_distribution(mc)

    one_hundred_KB_value = 'a' * 100000
    for i in range(0, 252):
        mc.set('small-{}'.format(i), one_hundred_KB_value)
    print_page_distribution(mc)


def print_page_distribution(memcache_client):
    slab_stats = {k: v for k, v in memcache_client.get_slab_stats()[0][1].items() if k.isdigit()}
    page_distribution = [(slab, stats['total_pages']) for slab, stats in slab_stats.items()]
    print(page_distribution)


if __name__ == '__main__':
    main()
