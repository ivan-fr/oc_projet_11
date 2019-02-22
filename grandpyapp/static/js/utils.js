// Exécute un appel AJAX POST
// Prend en paramètres l'URL cible, la donnée à envoyer et la fonction callback appelée en cas de succès
function ajaxPost(url, data, successCallback, errorCallback, generalCallback, progressCallback) {
    let req = new XMLHttpRequest();
    req.open("POST", url, true);
    req.addEventListener("load", function () {
        if (req.status >= 200 && req.status < 400) {
            // Appelle la fonction callback en lui passant la réponse de la requête
            successCallback(req.responseText);
        } else {
            errorCallback(req);
        }
        generalCallback();
    });
    req.addEventListener("progress", progressCallback);
    req.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    req.send(data);
}

function calculateAndDisplayRoute(start, end, directionsService, directionsDisplay, div_media, info_div) {
    directionsService.route({
        origin: {placeId: start},
        destination: end,
        travelMode: 'DRIVING'
    }, function (response, status) {
        if (status === 'OK') {
            info = response.routes[0].legs[0];
            info_div.innerHTML = "Distance : " + info.distance.text + "<br>" + "Durée : " + info.duration.text + " en voiture.";
            directionsDisplay.set('directions', null);
            directionsDisplay.setDirections(response);
            div_media.setAttribute('data-user-origin', start);
        } else {
            window.alert('Directions request failed due to ' + status);
        }
    });
}

let submit_ask_button = document.createElement("button");
submit_ask_button.type = "submit";
submit_ask_button.classList.add("btn");
submit_ask_button.classList.add("btn-primary");
submit_ask_button.classList.add("mb-2");
submit_ask_button.appendChild(document.createTextNode("Envoyer"));

let loader_img = document.createElement("div");
loader_img.classList.add("loader");

let block_submit_from_form = document.getElementById("submit_form");
block_submit_from_form.appendChild(submit_ask_button);

let ask_input = document.getElementById("ask");

let messagerie = document.createElement("ul");
messagerie.classList.add("list-unstyled");

function addMedia(title, message, src_media, nofirst) {
    let media = document.createElement("li");
    media.classList.add("media");
    if (nofirst) {
        media.classList.add("mt-4")
    }

    let image = document.createElement("img");
    image.src = src_media;
    image.classList.add("mr-3");
    image.width = "50";
    image.height = "50";

    let media_body = document.createElement("div");
    media_body.classList.add("media-body");

    let _title = document.createElement("h5");
    _title.classList.add("mt-0");
    _title.classList.add("mb-1");
    _title.appendChild(document.createTextNode(title));

    let div_media_body = document.createElement("div");

    let span_media_body = document.createElement("span");
    span_media_body.innerHTML = message;

    media_body.appendChild(_title);
    media_body.appendChild(span_media_body);
    media_body.appendChild(div_media_body);

    media.appendChild(image);
    media.appendChild(media_body);

    messagerie.appendChild(media);

    return media_body
}

let div_messagerie = document.getElementById("messagerie");
div_messagerie.appendChild(messagerie);

let span_messagerie = div_messagerie.getElementsByTagName("span")[0];

addMedia("GrandPy Bot",
    "Je suis un as de l'exploration. Questionne mon savoir.",
    span_messagerie.getAttribute("data-image-papi")
);

let messagerie_form = document.getElementById("messagerie-form");

// Gestion de la soumission du formulaire
messagerie_form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Récupération des champs du formulaire dans l'objet FormData
    let data = new FormData(messagerie_form);

    if (data.get("ask").trim() === "") {
        return
    }

    submit_ask_button.style.display = 'none';
    block_submit_from_form.appendChild(loader_img);
    ask_input.readOnly = "true";

    addMedia("Moi", data.get('ask'),
        span_messagerie.getAttribute("data-image-user"),
        true);

    div_messagerie.scrollTop = div_messagerie.scrollHeight - div_messagerie.clientHeight;

    ajaxPost(messagerie_form.action, data,
        function (responseText) {
            let obj = JSON.parse(responseText);

            try {
                let _location = new google.maps.LatLng(obj.google_maps_parsed.location.lat,
                    obj.google_maps_parsed.location.lng);

                let _location_northeast = new google.maps.LatLng(obj.google_maps_parsed.bounds.northeast.lat,
                    obj.google_maps_parsed.bounds.northeast.lng);

                let _location_southwest = new google.maps.LatLng(obj.google_maps_parsed.bounds.southwest.lat,
                    obj.google_maps_parsed.bounds.southwest.lng);

                let wiki_summary = obj.wikipedia_parsed._summary;

                if (wiki_summary === undefined) {
                    throw new Error("wiki non valide");
                }

                let media_body = addMedia("GrandPy Bot",
                    "Hum.. Je vois où celà se trouve !<br>" +
                    "Adresse: " + obj.google_maps_parsed.formatted_address,
                    span_messagerie.getAttribute("data-image-papi"),
                    true);

                let div_media_body = media_body.getElementsByTagName('div')[0];
                div_media_body.classList.add("map_canvas");

                let map = new google.maps.Map(div_media_body, {
                    mapTypeId: google.maps.MapTypeId.ROADMAP,
                });

                let marker = new google.maps.Marker({
                    position: _location,
                    map: map
                });

                let bounds = new google.maps.LatLngBounds();
                bounds.extend(_location_northeast);
                bounds.extend(_location_southwest);
                map.fitBounds(bounds);

                let button_trajet = document.createElement("button");
                button_trajet.classList.add("btn");
                button_trajet.classList.add("btn-primary");
                button_trajet.appendChild(document.createTextNode('Trajet'));


                let div_button_trajet = document.createElement("div");
                div_button_trajet.classList.add("row");

                let div_button_trajet_2 = document.createElement("div");
                div_button_trajet_2.classList.add("col-auto");

                div_button_trajet_2.appendChild(button_trajet);

                let div_button_trajet_3 = document.createElement("div");
                div_button_trajet_3.classList.add("col-auto");

                div_button_trajet.appendChild(div_button_trajet_2);
                div_button_trajet.appendChild(div_button_trajet_3);

                media_body.appendChild(div_button_trajet);

                let directionsService = new google.maps.DirectionsService();
                let directionsDisplay = new google.maps.DirectionsRenderer();

                directionsDisplay.setMap(map);

                button_trajet.addEventListener("click", function (e) {
                        e.preventDefault();

                        if (span_messagerie.getAttribute("data-user-origin")) {

                            let data_user_origin = span_messagerie.getAttribute("data-user-origin");

                            if (div_media_body.getAttribute("data-user-origin") !== data_user_origin) {
                                calculateAndDisplayRoute(data_user_origin, _location, directionsService, directionsDisplay, div_media_body, div_button_trajet_3);
                            }
                        } else {
                            window.alert('Entrez votre adresse pour avoir cette fonctionnalité.');
                        }
                    }
                );

                addMedia("GrandPy Bot",
                    "Tiens, ça me rappelle quelque chose: <br>" +
                    wiki_summary +
                    "<br><a href='" + obj.wikipedia_parsed.url + "' target='_blank'>[En savoir plus]</a>",
                    span_messagerie.getAttribute("data-image-papi"),
                    true);
            } catch (error) {
                addMedia("GrandPy Bot",
                    "Je suis vieux tu sais, formule moi ta question un peu plus simplement...",
                    span_messagerie.getAttribute("data-image-papi"),
                    true);
                console.error(error);
            }
            div_messagerie.scrollTop = div_messagerie.scrollHeight - div_messagerie.clientHeight;
        },
        function (req) {
            console.error(req.status + " " + req.statusText + " " + messagerie_form.action);
        },
        function () {
            setTimeout(function () {
                submit_ask_button.style.display = "block";
                ask_input.removeAttribute('readonly');
                ask_input.value = "";
                loader_img.parentNode.removeChild(loader_img);
                loader_img.removeAttribute("style");
            }, 1000);
        },
        function () {
            loader_img.style.borderBottom = "10px solid red";
            loader_img.style.borderTop = "10px solid red";
        }
    );
});

let adress_form = document.getElementById("adress_form");
let adress_result = document.getElementById("result-adress");
let adress_form_html = adress_result.innerHTML;
let adress_result_html = null;

function adress_form_listener(e) {
    e.preventDefault();

    let submit_inputs_block = e.target.querySelector(".form-row:last-child");
    let submit_inputs = submit_inputs_block.querySelectorAll(".form-group");

    for (let i = 0; i < submit_inputs.length; i++) {
        submit_inputs[i].style.display = 'none';
    }

    submit_inputs_block.appendChild(loader_img);

    let inputs_text_form = e.target.querySelectorAll("input[type=\"text\"]");

    for (let i = 0; i < inputs_text_form.length; i++) {
        inputs_text_form[i].readOnly = "true";
    }

    let errors_form = e.target.querySelectorAll(".list-error");

    Array.prototype.forEach.call(errors_form, function (element) {
        element.parentNode.removeChild(element);
    });

    // Récupération des champs du formulaire dans l'objet FormData
    let data = new FormData(e.target);

    ajaxPost(e.target.action, data,
        function (responseText) {
            let obj = JSON.parse(responseText);
            console.log(obj);
            if (obj.errors_form !== null) {
                obj.errors_form.forEach(function (element) {
                    let parent_input = document.getElementById(element[0]).parentNode;
                    let errors_ul = document.createElement("ul");
                    errors_ul.classList.add("list-error");
                    element[1].forEach(function (sub_element) {
                        let errors_li = document.createElement("li");
                        errors_li.appendChild(document.createTextNode(sub_element));
                        errors_ul.appendChild(errors_li);
                    });
                    parent_input.appendChild(errors_ul);
                });
            } else if (obj.google_maps_parsed !== null) {
                adress_result.innerHTML = "";
                let div_alert_green = document.createElement("div");
                div_alert_green.classList.add("alert");
                div_alert_green.classList.add("alert-success");
                div_alert_green.innerHTML = obj.google_maps_parsed.formatted_address + '. Place id : ' + obj.google_maps_parsed.place_id
                    + ' <a href="#">Modifier</a>';

                adress_result.appendChild(div_alert_green);
                adress_result_html = adress_result.innerHTML;

                function update_adress_listener(e) {
                    e.preventDefault();
                    adress_result.innerHTML = adress_form_html;
                    let a = adress_result.querySelectorAll("form .form-row");

                    let d = a[a.length - 1];

                    let b = document.createElement("div");
                    b.classList.add("form-group");
                    b.classList.add("col-md-auto");

                    let c = document.createElement("button");
                    c.classList.add("btn");
                    c.classList.add("btn-warning");
                    c.appendChild(document.createTextNode('Annuler'));

                    c.addEventListener("click", function (e) {
                        e.preventDefault();
                        adress_result.innerHTML = "";
                        adress_result.insertAdjacentHTML('afterbegin', adress_result_html);
                        adress_result.querySelector(".alert a").addEventListener("click", update_adress_listener);
                    });

                    adress_result.getElementsByTagName("form")[0].addEventListener("submit", adress_form_listener);

                    b.appendChild(c);
                    d.appendChild(b);
                }

                div_alert_green.getElementsByTagName('a')[0].addEventListener("click", update_adress_listener);

                span_messagerie.setAttribute("data-user-origin", obj.google_maps_parsed.place_id);
            }
        },
        function (req) {
            console.error(req.status + " " + req.statusText + " " + e.target.action);
        },
        function () {
            setTimeout(function () {
                for (let i = 0; i < submit_inputs.length; i++) {
                    submit_inputs[i].style.display = "block";
                }
                for (let i = 0; i < inputs_text_form.length; i++) {
                    inputs_text_form[i].removeAttribute('readonly');
                    inputs_text_form[i].value = "";
                }
                loader_img.parentNode.removeChild(loader_img);
                loader_img.removeAttribute("style");
            }, 1000);
        },
        function () {
            loader_img.style.borderBottom = "10px solid red";
            loader_img.style.borderTop = "10px solid red";
        }
    );
}

// Gestion de la soumission du formulaire
adress_form.addEventListener("submit", adress_form_listener);