Feature: Autenticacion de usuarios
  Como usuario
  Quiero poder registrarme, iniciar sesion y cerrar sesion
  Para poder acceder a las funcionalidades de la aplicacion

  Rule: Un usuario puede registrarse en la aplicacion
    Scenario: Registro exitoso
      Given que el usuario no esta autenticado
      When el usuario completa el formulario de registro con username "bauti" y password "auto123123"
      Then el usuario es redirigido al home estando autenticado

    Scenario: Registro fallido por password invalido
      Given que el usuario no esta autenticado
      When el usuario completa el formulario de registro con username "bauti" y password "123"
      Then el usuario ve un mensaje de error en el formulario de registro

  Rule: Un usuario puede iniciar sesion en la aplicacion
    Scenario: Login exitoso
      Given que existe un usuario registrado con username "bauti" y password "auto123123"
      When el usuario completa el formulario de login con username "bauti" y password "auto123123"
      Then el usuario es redirigido al home estando autenticado

    Scenario: Login fallido por credenciales incorrectas
      Given que existe un usuario registrado con username "bauti" y password "auto123123"
      When el usuario completa el formulario de login con username "bauti" y password "wrongpassword"
      Then el usuario ve un mensaje de error en el formulario de login

  Rule: Un usuario puede cerrar sesion en la aplicacion
    Scenario: Logout exitoso
      Given que el usuario completa el formulario de registro con username "bauti" y password "auto123123"
      And que el usuario completa el formulario de login con username "bauti" y password "auto123123"
      When el usuario cierra sesion
      Then el usuario es redirigido al home sin estar autenticado