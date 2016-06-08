===================
Using the tellstick
===================


Discovering devices
===================

On first run, you need to sync the devices with the one in telldusd :

.. code:: bash

    $ jnt_query node --hadd 0163/0000 --vuuid request_info_nodes

.. code:: bash

    request_info_nodes
    ----------
    hadd       uuid                           name                      location             product_type
    0163/0000  tellstick                      testname                  testlocation         Default product type

.. code:: bash

    $ jnt_query query --hadd 0163/0000 --genre command --uuid tellstick_discover --cmdclass 158 --writeonly True --data True

.. code:: bash

    $ jnt_query node --hadd 0163/0000 --vuuid request_info_nodes
    ----------
    hadd       uuid                           name                      location             product_type
    0163/0035  tellstick__35                  Detecteur mouvement SAM   Default location     Tellstick device
    0163/0019  tellstick__19                  Dimmer 2                  Default location     Tellstick device
    0163/0018  tellstick__18                  Dimmer 1                  Default location     Tellstick device
    0163/0038  tellstick__38                  Lampe Aquarium            Default location     Tellstick device
    0163/0034  tellstick__34                  Home cinema Chambre       Default location     Tellstick device
    0163/0013  tellstick__13                  Detecteur Porte Entree    Default location     Tellstick device
    0163/0012  tellstick__12                  Detecteur mouvement Entree Default location     Tellstick device
    0163/0037  tellstick__37                  Home Cinema SAM           Default location     Tellstick device
    0163/0010  tellstick__10                  Inter 1G                  Default location     Tellstick device
    0163/0017  tellstick__17                  B3                        Default location     Tellstick device
    0163/0016  tellstick__16                  B2                        Default location     Tellstick device
    0163/0015  tellstick__15                  B1                        Default location     Tellstick device
    0163/0032  tellstick__32                  plafonnier chambre        Default location     Tellstick device
    0163/0036  tellstick__36                  Dimmer Salle 2            Default location     Tellstick device
    0163/0031  tellstick__31                  Ambiance                  Default location     Tellstick device
    0163/0030  tellstick__30                  Table cuisine             Default location     Tellstick device
    0163/0033  tellstick__33                  Lampe chambre             Default location     Tellstick device
    0163/0028  tellstick__28                  Evier                     Default location     Tellstick device
    0163/0029  tellstick__29                  Plan de travail           Default location     Tellstick device
    0163/0026  tellstick__26                  Hotte cuisine             Default location     Tellstick device
    0163/0027  tellstick__27                  Hotte cuisine ambiance    Default location     Tellstick device
    0163/0024  tellstick__24                  Douille dimmer            Default location     Tellstick device
    0163/0025  tellstick__25                  Plafonnier SaM            Default location     Tellstick device
    0163/0022  tellstick__22                  Eclairage Bar             Default location     Tellstick device
    0163/0023  tellstick__23                  Inter Gen VR              Default location     Tellstick device
    0163/0020  tellstick__20                  Dimmer Salle 1            Default location     Tellstick device
    0163/0021  tellstick__21                  Bouton mobile             Default location     Tellstick device
    0163/0009  tellstick__9                   inter 1D                  Default location     Tellstick device
    0163/0008  tellstick__8                   Detecteur crepusculaire   Default location     Tellstick device
    0163/0007  tellstick__7                   Prise mobile              Default location     Tellstick device
    0163/0006  tellstick__6                   Lampe de chevet Chambre   Default location     Tellstick device
    0163/0005  tellstick__5                   VR Salle a manger         Default location     Tellstick device
    0163/0004  tellstick__4                   VR Cuisine                Default location     Tellstick device
    0163/0003  tellstick__3                   Plafonnier Cuisine        Default location     Tellstick device
    0163/0011  tellstick__11                  Tel C4                    Default location     Tellstick device
    0163/0000  tellstick                      testname                  testlocation         Default product type

All devices are discovered but in an unknown type. We should update them but it doesn't work :

.. code:: bash

    $ jnt_query query --hadd 0163/0004 --genre command --uuid tellstick_updatetype --cmdclass 158 --writeonly True --data tellstick_shutter

.. code:: bash

    fails

Stop the server and update your config file manually, matching device types depending on your installation :

.. code:: bash

    components.3 = tellstick.dimmer
    components.4 = tellstick.shutter
    components.5 = tellstick.shutter
    components.6 = tellstick.dimmer
    components.7 = tellstick.switch
    components.8 = tellstick.daylight
    components.9 = tellstick.remote
    components.10 = tellstick.remote
    components.11 = tellstick.remote
    components.12 = tellstick.pir
    components.13 = tellstick.magnetic
    components.15 = tellstick.remote
    components.16 = tellstick.remote
    components.17 = tellstick.remote
    components.18 = tellstick.dimmer
    components.19 = tellstick.dimmer
    components.20 = tellstick.dimmer
    components.21 = tellstick.remote
    components.22 = tellstick.switch
    components.23 = tellstick.remote
    components.24 = tellstick.dimmer
    components.25 = tellstick.switch
    components.26 = tellstick.switch
    components.27 = tellstick.switch
    components.28 = tellstick.switch
    components.29 = tellstick.switch
    components.30 = tellstick.switch
    components.31 = tellstick.switch
    components.32 = tellstick.switch
    components.33 = tellstick.dimmer
    components.34 = tellstick.switch
    components.35 = tellstick.pir
    components.36 = tellstick.dimmer
    components.37 = tellstick.switch
    components.38 = tellstick.switch

Restart the server and query it :

.. code:: bash

    $ jnt_query node --hadd 0163/0000 --vuuid request_info_nodes

.. code:: bash

    request_info_nodes
    ----------
    hadd       uuid                           name                      location             product_name              product_type
    0163/0035  tellstick__35                  Detecteur mouvement SAM   Default location     Tellstick pir             Tellstick device
    0163/0019  tellstick__19                  Dimmer 2                  Default location     Tellstick dimmer          Tellstick device
    0163/0018  tellstick__18                  Dimmer 1                  Default location     Tellstick dimmer          Tellstick device
    0163/0038  tellstick__38                  Lampe Aquarium            Default location     Tellstick switch          Tellstick device
    0163/0034  tellstick__34                  Home cinema Chambre       Default location     Tellstick switch          Tellstick device
    0163/0013  tellstick__13                  Detecteur Porte Entree    Default location     Tellstick magnetic        Tellstick device
    0163/0012  tellstick__12                  Detecteur mouvement Entree Default location     Tellstick pir             Tellstick device
    0163/0037  tellstick__37                  Home Cinema SAM           Default location     Tellstick switch          Tellstick device
    0163/0036  tellstick__36                  Dimmer Salle 2            Default location     Tellstick dimmer          Tellstick device
    0163/0031  tellstick__31                  Ambiance                  Default location     Tellstick switch          Tellstick device
    0163/0030  tellstick__30                  Table cuisine             Default location     Tellstick switch          Tellstick device
    0163/0033  tellstick__33                  Lampe chambre             Default location     Tellstick dimmer          Tellstick device
    0163/0032  tellstick__32                  plafonnier chambre        Default location     Tellstick switch          Tellstick device
    0163/0010  tellstick__10                  Inter 1G                  Default location     Tellstick sensor          Tellstick device
    0163/0017  tellstick__17                  B3                        Default location     Tellstick sensor          Tellstick device
    0163/0016  tellstick__16                  B2                        Default location     Tellstick sensor          Tellstick device
    0163/0015  tellstick__15                  B1                        Default location     Tellstick sensor          Tellstick device
    0163/0028  tellstick__28                  Evier                     Default location     Tellstick switch          Tellstick device
    0163/0029  tellstick__29                  Plan de travail           Default location     Tellstick switch          Tellstick device
    0163/0026  tellstick__26                  Hotte cuisine             Default location     Tellstick switch          Tellstick device
    0163/0027  tellstick__27                  Hotte cuisine ambiance    Default location     Tellstick switch          Tellstick device
    0163/0024  tellstick__24                  Douille dimmer            Default location     Tellstick dimmer          Tellstick device
    0163/0025  tellstick__25                  Plafonnier SaM            Default location     Tellstick switch          Tellstick device
    0163/0022  tellstick__22                  Eclairage Bar             Default location     Tellstick switch          Tellstick device
    0163/0023  tellstick__23                  Inter Gen VR              Default location     Tellstick sensor          Tellstick device
    0163/0020  tellstick__20                  Dimmer Salle 1            Default location     Tellstick dimmer          Tellstick device
    0163/0021  tellstick__21                  Bouton mobile             Default location     Tellstick sensor          Tellstick device
    0163/0009  tellstick__9                   inter 1D                  Default location     Tellstick sensor          Tellstick device
    0163/0008  tellstick__8                   Detecteur crepusculaire   Default location     Tellstick daylight        Tellstick device
    0163/0007  tellstick__7                   Prise mobile              Default location     Tellstick switch          Tellstick device
    0163/0006  tellstick__6                   Lampe de chevet Chambre   Default location     Tellstick dimmer          Tellstick device
    0163/0005  tellstick__5                   VR Salle a manger         Default location     Tellstick shutter         Tellstick device
    0163/0004  tellstick__4                   VR Cuisine                Default location     Tellstick shutter         Tellstick device
    0163/0003  tellstick__3                   Plafonnier Cuisine        Default location     Tellstick dimmer          Tellstick device
    0163/0011  tellstick__11                  Tel C4                    Default location     Tellstick sensor          Tellstick device
    0163/0000  tellstick                      testname                  testlocation         Tellstick bus controller  Default product type

Update a switch :

.. code:: bash

    $ jnt_query query --hadd 0163/0038 --genre user --uuid switch --cmdclass 37 --writeonly True --data on

Or a dimmer :

.. code:: bash

    $ jnt_query query --hadd 0163/0003 --genre user --uuid switch --cmdclass 37 --writeonly True --data on

    $ jnt_query query --hadd 0163/0003 --genre user --uuid dim --cmdclass 38 --writeonly True --data 60

    $ jnt_query query --hadd 0163/0003 --genre user --uuid switch --cmdclass 37 --writeonly True --data off

And for shutters :

.. code:: bash

    $ jnt_query query --hadd 0163/0005 --genre user --uuid shutter --cmdclass 12624 --writeonly True --data down

    $ jnt_query query --hadd 0163/0005 --genre user --uuid shutter --cmdclass 12624 --writeonly True --data stop

    $ jnt_query query --hadd 0163/0005 --genre user --uuid shutter --cmdclass 12624 --writeonly True --data up

Performances
============

On a raspberry pi 2:

.. code:: bash

  PID USER      PR  NI  VIRT  RES  SHR S  %CPU %MEM    TIME+  COMMAND
  752 root      20   0 96700  17m 5408 S   7,2  3,6   1:05.05 /usr/bin/python /usr/local/bin/jnt_tellstick -c /opt/janitoo/src/janitoo_tellstick/tests/data/ja
