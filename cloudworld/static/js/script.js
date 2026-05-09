$(document).ready(function () {

    $("#contactForm").submit(function (event) {

        event.preventDefault();

        let isValid = true;

        $(".error-message").hide();
        $(".form-control").removeClass("is-invalid");


        if ($("#nombre").val().trim() === "") {

            $("#nombre").addClass("is-invalid");

            $("#nombre")
                .next(".error-message")
                .text("El nombre es obligatorio")
                .show();

            isValid = false;
        }


        let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (
            $("#email").val().trim() === "" ||
            !emailPattern.test($("#email").val())
        ) {

            $("#email").addClass("is-invalid");

            $("#email")
                .next(".error-message")
                .text("Por favor ingresar email valido")
                .show();

            isValid = false;
        }


        let telefonoRegex = /^[0-9]+$/;

        if (
            $("#telefono").val().trim() === "" ||
            !telefonoRegex.test($("#telefono").val())
        ) {

            $("#telefono").addClass("is-invalid");

            $("#telefono")
                .next(".error-message")
                .text("El telefono es obligatorio")
                .show();

            isValid = false;
        }


        if (!$("#terminos").is(":checked")) {

            $("#terminos").addClass("is-invalid");

            $("#terminos")
                .next(".error-message")
                .text("Debe aceptar los terminos")
                .show();

            isValid = false;
        }


        if (isValid) {

            alert("Formulario enviado correctamente!");
            $("#contactForm")[0].reset();
        }

    });


    $("#terminos").change(function () {

        $(this).removeClass("is-invalid");

        $(this)
            .closest(".form-check")
            .find(".error-message")
            .hide();
    });


    $("#registroForm").submit(function (event) {

        let valido = true;

        $(".error-message").text("");
        $(".form-control").removeClass("is-invalid");


        let username = $("#id_username").val().trim();

        if (username.length < 5) {

            $("#id_username").addClass("is-invalid");

            $("#id_username")
                .closest(".mb-3")
                .find(".error-message")
                .text("El usuario debe tener minimo 5 caracteres");

            valido = false;
        }


        let email = $("#id_email").val().trim();

        let emailRegex2 = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex2.test(email)) {

            $("#id_email").addClass("is-invalid");

            $("#id_email")
                .closest(".mb-3")
                .find(".error-message")
                .text("Ingrese un email valido");

            valido = false;
        }


        let password = $("#id_password").val();

        if (password.length < 8) {

            $("#id_password").addClass("is-invalid");

            $("#id_password")
                .closest(".mb-3")
                .find(".error-message")
                .text("La contraseña debe tener minimo 8 caracteres");

            valido = false;
        }


        if (!valido) {
            event.preventDefault();
        }

    });

});