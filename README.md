## Synopsis

digitalocean-droplet-manager is a Python command-line interface for automated
creation and destruction of DigitalOcean droplets.

## Requirements

In order for this program to function, fully, a domain should be pre-created
for this droplet. This only needs to be done once. Then, delete the A record
associated with it before using `create`. This will hopefully be streamlined in
the future if I bother to continue working on this.

## Examples

To run digitalocean-droplet-manager, simply download and install the
requirements via pip:

```bash
pip install -r requirements.txt
```

Once this is done, `domanager.py` can be run. It currently has two commands,
`create` and `destroy`. Both of these take a single argument, which is a
configuration file to use. A sample configuration file is provided as
`sample.cfg`. Before it will work, a DigitalOcean API token must be inserted
into the file.

To create a droplet based on the configuration:

```bash
python domanager.py create something.cfg
```

To destroy the droplet:

```bash
python domanager.py destroy something.cfg
```

## Motivation

DigitalOcean charges for droplets by the hour. I wanted an easy way to tear
down and restore images, but there were a few problems with snapshots:

1. The IP changes every time the box resumes, so the domain name would fail.
2. ssh keys weren't automatically added back
3. Restoration required the web UI and more than one click (I'm lazy)

Thus, to solve this problem, you can use this tool, create a single
specification, then create/destroy whenever you want, conveniently, with the
same commands.

## Installation

TBD

## API Reference

TBD

## Tests

TBD

## Contributors

Still working out the kinks, and uploaded to GitHub as a backup mechanism. Not
looking for feedback or issues yet!

## License

MIT License. See LICENSE.
