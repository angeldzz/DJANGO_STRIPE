let acceso = "";
let refresco = "";
let articuloIdModificando = null; // Variable para almacenar el ID del artículo que se está modificando

async function autorizar() {
    try {
        let response = await fetch('http://127.0.0.1:8000/api/token/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: $('#usuario').val(),
                password: $('#passwd').val(),
            })
        });

        let data = await response.json();

        if (!response.ok) {
            alert("Error en la autenticación: " + (data.detail || "Credenciales incorrectas"));
            return;
        }

        autorizado(data);
    } catch (error) {
        alert("Error con el usuario :" + error);
    }    
}

function autorizado(data) {
    acceso = data.access;
    refresco = data.refresh;

    $("#formAutorizar").addClass('d-none');
    $("#cuerpo").removeClass('d-none');

    recogerArticulos();
}

function recogerArticulos() {
    console.log("listaArticulos");
    fetch("http://127.0.0.1:8000/api/articulos/", {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${acceso}`,
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => listarArticulos(data))
    .catch(error => console.log("Error de fetch api/articulos: " + error));
}

function listarArticulos(datos) {
    $("#cuerpoTabla").empty();
    const template = $("#filaArticulo")[0];
    datos.forEach(dato => { 
        const fila = template.content.cloneNode(true);

        $(fila).find("slot[name='titulo']").replaceWith(dato["titulo"]);
        $(fila).find("slot[name='fecha_pub']").replaceWith(new Date(dato["fecha_publicacion"]).toLocaleDateString("es-ES", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric"
        }));
        $(fila).find("slot[name='autor']").replaceWith(dato["autor"]);
        $(fila).find("slot[name='detalles']").replaceWith($("<button>",
            {text:"Detalles",type:"button",class:"btn btn-warning",onclick:`mostrarDetalles(${dato.id})`}));

        $(fila).find("slot[name='modificar']").replaceWith($("<button>",
            {text:"Modificar",type:"button",class:"btn btn-primary",onclick:`cargarDatosModificar(${dato.id}, '${dato.titulo}', '${dato.contenido}')`}));
        $(fila).find("slot[name='eliminar']").replaceWith($("<button>",
            {text:"Borrar",type:"button",class:"btn btn-danger",onclick:`borrarArticulo(${dato.id})`}));
        $("#cuerpoTabla").append(fila);
    });
}

function crearArticulo() {
    // Recoger los datos del formulario
    const articuloData = {
        titulo: $("#titulo").val(),
        contenido: $("#contenido").val()
    };

    // Realizar el fetch con el token access
    fetch("http://127.0.0.1:8000/api/articulos/", {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${acceso}`, // Usamos la variable global acceso
            "Content-Type": "application/json"
        },
        body: JSON.stringify(articuloData)
    })
    .then(response => response.json())
    .then(data => {
        // Éxito: Mostrar mensaje y limpiar formulario
        $("#mensajeRespuesta").html('<div class="alert alert-success">Artículo creado exitosamente</div>');
        recogerArticulos(); // Actualizar la lista de artículos
    })
    .catch(error => {
        // Error: Mostrar mensaje de error
        $("#mensajeRespuesta").html(`<div class="alert alert-danger">${error.message}</div>`);
        console.error("Error al crear artículo:", error);
    });
}

function cancelarModificar() {
    $("#crearArticulo").show(); 
    $("#modificarArticulo").hide(); 
    $("#cancelarModificar").hide();
    $("#titulo").val(""); 
    $("#contenido").val("");
}

function cargarDatosModificar(id, titulo, contenido) {
    articuloIdModificando = id; // Guardamos el ID del artículo a modificar
    $("#titulo").val(titulo); // Rellenamos el campo título
    $("#contenido").val(contenido); // Rellenamos el campo contenido
    $("#crearArticulo").hide(); // Ocultamos el botón "Crear" mientras modificamos
    $("#modificarArticulo").show(); // Mostramos el botón "Modificar"
    $("#cancelarModificar").show();
}

function modificarArticulo() {
    if (!articuloIdModificando) {
        $("#mensajeRespuesta").html('<div class="alert alert-warning">Selecciona un artículo para modificar primero</div>');
        return;
    }

    fetch(`http://127.0.0.1:8000/api/articulos/${articuloIdModificando}/`, {
        method: "PUT",
        headers: {
            "Authorization": `Bearer ${acceso}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            titulo: $("#titulo").val(),
            contenido: $("#contenido").val()
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.detail || "Error al modificar el artículo");
            });
        }
        return response.json();
    })
    .then(data => {
        $("#mensajeRespuesta").html('<div class="alert alert-success">Artículo modificado exitosamente</div>');
        $("#titulo").val(""); // Limpiamos manualmente
        $("#contenido").val("");
        articuloIdModificando = null; // Reseteamos el ID
        $("#crearArticulo").show(); // Mostramos de nuevo el botón "Crear"
        $("#modificarArticulo").hide(); // Ocultamos el botón "Modificar"
        $("#cancelarModificar").hide(); // Ocultamos el botón "Cancelar Modificar"
        recogerArticulos();
    })
    .catch(error => {
        $("#mensajeRespuesta").html(`<div class="alert alert-danger">${error.message}</div>`);
        console.error("Error al modificar artículo:", error);
    });
}

function mostrarDetalles(id) {
    fetch(`http://127.0.0.1:8000/api/articulos/${id}/`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${acceso}`,
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        $("#detalle").empty();
        const detallesHtml = `
            <h2>${data.titulo}</h2>
            <p><strong>Autor:</strong> ${data.autor}</p>
            <p><strong>Fecha de publicación:</strong> ${new Date(data.fecha_publicacion).toLocaleDateString("es-ES", {
                day: "2-digit",
                month: "2-digit",
                year: "numeric"
            })}</p>
            <p><strong>Contenido:</strong> ${data.contenido}</p>
        `;
        $("#detalle").html(detallesHtml);
    })
    .catch(error => {
        $("#detalle").html(`<div class="alert alert-danger">${error.message}</div>`);
        console.error("Error al mostrar detalles:", error);
    });
}

function borrarArticulo(id) {
    fetch(`http://127.0.0.1:8000/api/articulos/${id}/`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${acceso}`,
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        console.log("Articulo borrado");
        recogerArticulos();
    })
    .catch(error => console.error("Error: " + error));
}

// Vincular eventos
$("#crearArticulo").on("click", () => crearArticulo());
$("#modificarArticulo").on("click", () => modificarArticulo());
$("#cancelarModificar").on("click", () => cancelarModificar());

// Inicialmente ocultamos el botón "Modificar" hasta que se seleccione un artículo
$("#modificarArticulo").hide();
$("#cancelarModificar").hide();