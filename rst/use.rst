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

    $ jnt_query node --hadd 0163/0000 --vuuid request_info_nodesrequest_info_nodes
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

All devices are discovered but in an unknown type. We should update them :

.. code:: bash

    $ jnt_query query --hadd 0163/0004 --genre command --uuid tellstick_updatetype --cmdclass 158 --writeonly True --data tellstick_shutter

.. code:: bash

    fails
