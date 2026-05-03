$(document).ready(function () {
    // Validación al enviar el formulario
    $("#contactForm").submit(function (event) {
        event.preventDefault();

        let isValid = true;

        // Ocultar mensajes de error y quitar clases
        $(".error-message").hide();
        $(".form-control").removeClass("is-invalid");

        // Validar Nombre
        if ($("#nombre").val().trim() === "") {
            $("#nombre").addClass("is-invalid");
            $("#nombre").next(".error-message").text("El nombre es obligatorio.").show();
            isValid = false;
        }

        // Validar Email
        let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if ($("#email").val().trim() === ""|| !emailPattern.test($("#email").val())) {
            $("#email").addClass("is-invalid");
            $("#email").next(".error-message").text("Por favor ingresar email correctamente.").show();
            isValid = false;
        }

        // Validar Teléfono (solo números)
        let telefonoRegex = /^[0-9]+$/;
        if ($("#telefono").val().trim() === "" || !telefonoRegex.test($("#telefono").val())) {
            $("#telefono").addClass("is-invalid");
            $("#telefono").next(".error-message").text("El teléfono es obligatorio.").show();
            isValid = false;
        }

        // Validar Checkbox
        if (!$("#terminos").is(":checked")) {
            $("#terminos").addClass("is-invalid");
            $("#terminos").next(".error-message").text("Solo se permirten numeros.").show();
            isValid = false;
        }

        // Si todo es válido
        if (isValid) {
            alert("Formulario enviado correctamente!");
            $("#contactForm")[0].reset();
        }
    });
    
    // Quitar error al marcar el checkbox - papito dios es grande porque me funciono
    $("#terminos").change(function(){
        $(this).removeClass("is-invalid");
        $(this).closest(".form-check").find(".error-message").hide();
    });
});
