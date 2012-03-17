Sunzi-sudo
==========

Sunzi-sudo is a wrapper for [Sunzi](https://github.com/kenn/sunzi).

Quickstart
----------

Install

```bash
$ git clone https://github.com/heavensehell/sunzi-sudo.git
```

Sunzi-sudo depends on Python Fabric.

```bash
$ sudo pip install fabric
```

Usage

```bash
$ fab sunzi:foo@example.com
```

If you use [Bundler](http://gembundler.com/), you can add bundle option.

```bash
$ fab sunzi:bundle,foo@example.com
```

Deploy to multipul hosts.

```bash
$ fab sunzi:bundle,user=foo -H a.example.com b.example.com
```

This command deploys to `foo@a.example.com` and `foo@b.example.com`.

You can also type following.

```bash
$ fab sunzi:bundle -u foo -H 1.example.com 2.example.com
```
