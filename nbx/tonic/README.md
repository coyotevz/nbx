Tonic
=====

Resource
--------

Un `Resource` construye y almacena toda la información pertinente al manejo de
un recurso a travez de una interfaz REST.
Entre otras cosas las piezas importantes de un `Resource` son:

    - modelo al que representa
      A travez de la interfaz el `Resource` crea, modifica y elimina instancias
      del modelo al que representa.

    - schema
      Es donde se define como van a ser la forma de los datos de
      entrada y de salida en la comunicación con el mundo exterior, el trabajo
      de definir estas formas se lo delegamos a la libreria `marshmallow`, que
      basados en el modelo que vamos a representar elabora un schema.

    - rules, es un conjunto de rutas, endpoints y view_funcs que en forma
      conjunta indican que porcion de codigo ejecutar??? malisimo

        - rutas
          El objeto `Resource` genera las rutas necesarias para interacturar
          con el cliente de la interfaz, estas rutas se generan siguendo el
          patrón REST.

        - endpoint
          Es el nombre que se le asigna a la relación de la ruta con la view_func

        - view_func
          El la función que se ejecuta cuando el cliente alcanza una
          determinada ruta bajo ciertas condiciones
