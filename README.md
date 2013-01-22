Using
=====

To use this plugin:

* build it:

        mkdir -p /tmp/github
        cd /tmp/github
        git clone git://github.com/supermanvelo/morituri-whatcd.git
        cd morituri-whatcd
        python setup.py bdist_egg

* copy it to your plugin directory:

        mkdir -p $HOME/.morituri/plugins
        cp dist/morituri_*egg $HOME/.morituri/plugins

* verify that it gets recognized:

        rip cd rip --help

   You should see whatcd as a possible logger.

* use it:

        rip cd rip --logger=whatcd


Developers
==========

To use the plugin while developing uninstalled:

    python setup.py develop --install-dir=path/to/checkout/of/morituri
