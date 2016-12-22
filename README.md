---
layout: post
title: "Memcached"
date: 2016-12-14
---

Todo:

* Add image of how memcache uses memory (pages, slabs, chunks)
* example with autoallocatin turned off and getting into a bad state
* run same example with autoallocation turned on
* example with multiple instances
* example with reprecache to add replicas (how failover works)
* how to scale

The following was done on Ubuntu 14.04.1.

# Installation

```bash
sudo apt-get install memcached
```

and it seemed to start automatically,

```bash
$ ps -ax | grep memcached
11760 ?        Sl     0:00 /usr/bin/memcached -m 64 -p 11211 -u memcache -l 127.0.0.1
```

memcached can be controlled via,

```
sudo service memcached start|stop|status
```

and the configuration can be found in `/etc/memcached.conf`.

Commands can be sent to memcached from the command line using netcat,

```bash
$ echo "version" | nc 127.0.0.1 11211
VERSION 1.4.14 (Ubuntu)
```

## How the cache grows


## Reassignment of slabs

To allow reassignment of slabs (a feature introduced in [v1.4.11](https://github.com/memcached/memcached/wiki/ReleaseNotes1411)
I added the following line to `/etc/memcached.conf` and restarted the
memcached server (slab reassignment can only be enabled at start time).

```
-o slab_reassign
```

Automove can be enabled by specifying an option on startup (`slab_automove`)
or the following command,

```bash
echo "slabs automove 1" | nc localhost 11211
```

A demonstration of automove can be seen by running the `get_stats.py`
file in the repo (output shown below),

```bash
$ python get_stats.py 
Disabled autmove
{'32': {'total_pages': '6', 'cmd_set': '120000', 'evicted': '119940'}, '40': {'total_pages': '59', 'cmd_set': '300', 'evicted': '236'}}
Fill cache with 500KB items
{'32': {'total_pages': '6', 'cmd_set': '120000', 'evicted': '119940'}, '40': {'total_pages': '59', 'cmd_set': '450', 'evicted': '386'}}
Start adding 100KB items
{'32': {'total_pages': '6', 'cmd_set': '122000', 'evicted': '121940'}, '40': {'total_pages': '59', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '6', 'cmd_set': '124000', 'evicted': '123940'}, '40': {'total_pages': '59', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '6', 'cmd_set': '126000', 'evicted': '125940'}, '40': {'total_pages': '59', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '6', 'cmd_set': '128000', 'evicted': '127940'}, '40': {'total_pages': '59', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '6', 'cmd_set': '130000', 'evicted': '129940'}, '40': {'total_pages': '59', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '6', 'cmd_set': '132000', 'evicted': '131940'}, '40': {'total_pages': '59', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '6', 'cmd_set': '134000', 'evicted': '133940'}, '40': {'total_pages': '59', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '6', 'cmd_set': '136000', 'evicted': '135940'}, '40': {'total_pages': '59', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '6', 'cmd_set': '138000', 'evicted': '137940'}, '40': {'total_pages': '59', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '6', 'cmd_set': '140000', 'evicted': '139940'}, '40': {'total_pages': '59', 'cmd_set': '450', 'evicted': '386'}}
Enabled automove
{'32': {'total_pages': '6', 'cmd_set': '142000', 'evicted': '141940'}, '40': {'total_pages': '59', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '6', 'cmd_set': '144000', 'evicted': '143940'}, '40': {'total_pages': '59', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '6', 'cmd_set': '146000', 'evicted': '145940'}, '40': {'total_pages': '59', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '6', 'cmd_set': '148000', 'evicted': '147940'}, '40': {'total_pages': '59', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '6', 'cmd_set': '150000', 'evicted': '149940'}, '40': {'total_pages': '59', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '6', 'cmd_set': '152000', 'evicted': '151940'}, '40': {'total_pages': '59', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '6', 'cmd_set': '154000', 'evicted': '153940'}, '40': {'total_pages': '59', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '7', 'cmd_set': '156000', 'evicted': '155930'}, '40': {'total_pages': '58', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '7', 'cmd_set': '158000', 'evicted': '157930'}, '40': {'total_pages': '58', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '8', 'cmd_set': '160000', 'evicted': '159920'}, '40': {'total_pages': '57', 'cmd_set': '450', 'evicted': '386'}}
Disabled autmove
{'32': {'total_pages': '8', 'cmd_set': '162000', 'evicted': '161920'}, '40': {'total_pages': '57', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '8', 'cmd_set': '164000', 'evicted': '163920'}, '40': {'total_pages': '57', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '8', 'cmd_set': '166000', 'evicted': '165920'}, '40': {'total_pages': '57', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '8', 'cmd_set': '168000', 'evicted': '167920'}, '40': {'total_pages': '57', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '8', 'cmd_set': '170000', 'evicted': '169920'}, '40': {'total_pages': '57', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '8', 'cmd_set': '172000', 'evicted': '171920'}, '40': {'total_pages': '57', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '8', 'cmd_set': '174000', 'evicted': '173920'}, '40': {'total_pages': '57', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '8', 'cmd_set': '176000', 'evicted': '175920'}, '40': {'total_pages': '57', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '8', 'cmd_set': '178000', 'evicted': '177920'}, '40': {'total_pages': '57', 'cmd_set': '450', 'evicted': '386'}}
{'32': {'total_pages': '8', 'cmd_set': '180000', 'evicted': '179920'}, '40': {'total_pages': '57', 'cmd_set': '450', 'evicted': '386'}}
```

## References
* http://balodeamit.blogspot.co.uk/2014/02/slab-reallocation-in-memcache.html
