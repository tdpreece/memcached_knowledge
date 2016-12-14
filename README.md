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


```bash
echo "slabs automove 0" | nc localhost 11211
```



