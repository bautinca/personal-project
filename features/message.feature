Feature: Mensajes en salas
  Como usuario
  Quiero poder enviar mensajes en una sala
  Para poder comunicarme con otros usuarios

  Background: Usuario registrado y logeado
    Given que el usuario completa el formulario de registro con username "bauti" y password "auto123123"
    And que el usuario completa el formulario de login con username "bauti" y password "auto123123"
    And que el usuario crea una sala con nombre "Sala Python" y topic "Programacion" y descripcion "Una sala de Python"

  Rule: Solo usuarios registrados pueden enviar mensajes en una sala
    Scenario: Usuario registrado envia un mensaje en una sala
      When el usuario entra a la sala "Sala Python" y envia el mensaje "Hola a todos!"
      Then el mensaje "Hola a todos!" aparece en la sala "Sala Python"

    Scenario: Usuario no registrado no ve el formulario para enviar mensajes
      Given que el usuario no esta autenticado
      When el usuario no registrado entra a la sala "Sala Python"
      Then no ve el formulario para enviar mensajes