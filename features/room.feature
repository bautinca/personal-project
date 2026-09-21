Feature: Gestion de salas
  Como usuario
  Quiero gestionar salas
  Para poder crear, editar y eliminar salas

  Rule: Todo usuario registrado y logeado puede crear una sala
    Scenario: Crear una sala
      Given que el usuario completa el formulario de registro con username "bauti" y password "auto123123"
      And que el usuario completa el formulario de login con username "bauti" y password "auto123123"
      When el usuario completa el formulario de crear sala con nombre "Sala Python" y topic "Programacion" y descripcion "Una sala de Python"
      Then el usuario es redirigido al home y ve la sala "Sala Python" en la lista

    Scenario: Usuario no registrado intenta crear una sala
      Given que el usuario no esta autenticado
      When el usuario intenta acceder a la pagina de crear sala
      Then es redirigido a la pagina de login

  Rule: Solo el host puede editar una sala
    Scenario: Host edita su propia sala
      Given que el usuario completa el formulario de registro con username "bauti" y password "auto123123"
      And que el usuario completa el formulario de login con username "bauti" y password "auto123123"
      And que el usuario crea una sala con nombre "Sala Python" y topic "Programacion" y descripcion "Una sala de Python"
      When el host edita la sala "Sala Python" cambiando el nombre a "Sala Django" y topic "Programacion" y descripcion "Una sala de Django"
      Then el usuario es redirigido al home y ve la sala "Sala Django" en la lista
    
    Scenario: Usuario no host intenta editar una sala
      Given que el usuario completa el formulario de registro con username "bauti" y password "auto123123"
      And que el usuario completa el formulario de login con username "bauti" y password "auto123123"
      And que el usuario crea una sala con nombre "Sala Python" y topic "Programacion" y descripcion "Una sala de Python"
      And que el usuario completa el formulario de registro con username "otro" y password "auto123123"
      And que el usuario completa el formulario de login con username "otro" y password "auto123123"
      When el usuario no host ve la lista de salas
      Then no ve la opcion de editar la sala "Sala Python"

  Rule: Solo el host puede eliminar una sala
    Scenario: host elimina su propia sala
      Given que el usuario completa el formulario de registro con username "bauti" y password "auto123123"
      And que el usuario completa el formulario de login con username "bauti" y password "auto123123"
      And que el usuario crea una sala con nombre "Sala Python" y topic "Programacion" y descripcion "Una sala de Python"
      When el host le da click al boton de eliminar de la sala "Sala Python"
      Then la sala "Sala Python" no aparece en la lista de salas

    Scenario: Usuario no host no ve la opcion de eliminar una sala
      Given que el usuario completa el formulario de registro con username "bauti" y password "Xk9#mPqL2w"
      And que el usuario completa el formulario de login con username "bauti" y password "Xk9#mPqL2w"
      And que el usuario crea una sala con nombre "Sala Python" y topic "Programacion" y descripcion "Una sala de Python"
      And que el usuario completa el formulario de registro con username "otro" y password "Xk9#mPqL2w"
      And que el usuario completa el formulario de login con username "otro" y password "Xk9#mPqL2w"
      When el usuario no host ve la lista de salas
      Then no ve la opcion de eliminar la sala "Sala Python"