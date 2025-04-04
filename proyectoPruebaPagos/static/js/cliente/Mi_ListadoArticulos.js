let actualizador = $("#actualizador")
let token = localStorage.getItem("token");

//esto es una tonteria para cambiar entre ver o no la contraseña
document.getElementById("togglePassword").addEventListener("click", function() {
    const passwordInput = document.getElementById("password");
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        this.innerText = "👁️";
    } else {
        passwordInput.type = "password";
        this.innerText = "🙈";
    }
});
function verificarToken () {
    //verificamos el token y la respuesta tiene que ser valida para cargar el token
    console.log("vamos a verificar el token");
    fetch('http://127.0.0.1:8000/api/token/verify/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            token: token
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data){
            cargarToken();
        }else{
            console.log("token no valido");
        }
    })
    .catch(error => console.error('Error:', error));
}

$("#cargarToken").on("click",() => cargarToken())

async function cargarToken() {
token = localStorage.getItem("token");
    if (!token || token == undefined || token == "") {
        let user = $("#usuario").val();
        let pass = $("#password").val();

        try {
            let response = await fetch("http://127.0.0.1:8000/api/token/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: user,
                    password: pass
                })
            });

            let data = await response.json();
            if (data.access) {
            localStorage.setItem("token", data.access);
            verificarToken();
            cargarArticulos();
            } else {
                throw new Error("No se recibió un token válido");
            }
        } catch (error) {
            console.error("Token no valido");
            console.error("Error al obtener el token:", error);
            $("#actualizador").html(`
            <div class="col-3"></div>
            <div class="col-6">
                <form class="p-4 bg-light rounded shadow-sm text-center">
                    <div class="mb-3">
                        <label for="usuario" class="form-label">Usuario</label>
                        <input type="text" class="form-control" id="usuario" placeholder="Ingresa tu usuario" required>
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Contraseña</label>
                        <div class="input-group">
                            <input type="password" class="form-control" id="password" placeholder="Ingresa tu contraseña" required>
                            <button class="btn btn-outline-secondary" type="button" id="togglePassword">
                                🙈
                            </button>
                        </div>
                    </div>
                    <button id="cargarToken" type="button" class="btn btn-primary">Iniciar Sesión</button>
                </form>
            </div>
            <div class="col-3"></div>
        `);
        }
    }else{
        cargarArticulos();
    }
}
function cargarArticulos () {
    //hacemos fetch para coger los articulos con el token
    fetch("http://127.0.0.1:8000/api/articulos/", {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => creartablaArticulos(data))
    .catch(error => console.log("Error de fetch api/articulos: " + error));
}
function creartablaArticulos(datos) {
    //funcion para crear la tabla de articulos si tiene token
    //Intervalo para comprobar el token cada minuto
    setInterval(function() {
        verificarToken();
    }, 60000);
    actualizador.html(`
        <div class="col-3"></div>
        <div class="col-6">
            <table class="table table-striped text-center">
                <thead class="thead thead-dark">
                    <tr>
                        <th>Titulo</th>
                        <th>Fecha de Publicacion</th>
                        <th>Autor</th>
                    </tr>
                </thead>
                <tbody id="cuerpoTabla"></tbody>
            </table>
        </div>
        <div class="col-3"></div>
        `)
    datos.forEach(dato =>{ 
        let tr = $("<tr>")
        tr.on("click",() => recogerArticulo(dato.id))

        let tdTitulo = $("<td>",{
            text:dato["titulo"],
        });
        
        let tdFecha_P = $("<td>",{
            text: new Date(dato["fecha_publicacion"]).toLocaleDateString("es-ES", {
                day: "2-digit",
                month: "2-digit",
                year: "numeric"
            })
        });
        let td_Autor = $("<td>",{
            text:dato["autor"]
        });
    let tabla = $("#cuerpoTabla");
    tabla.append(tr.append(tdTitulo,tdFecha_P,td_Autor))
    });
}
function recogerArticulo(id) {
    //hacemos fetch para coger datos del articulo concreto
    fetch(`http://127.0.0.1:8000/api/articulos/${id}/`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log("Error de fetch api/articulos: " + error));
}
function detalleArticulo(datosArticulo) {
    // Recogemos los detalles del articulo seleccionado
    console.log(datosArticulo);
}
//si el token no es null lo verificamos
if(token != null){
    verificarToken();
}