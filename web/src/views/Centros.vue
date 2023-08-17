<template>
  <div class="centros">
    <section class="container border border-light p-5 text-left">
      <h1 class="text-left">Crear un centro</h1>
      <br/>
      <form>
        <p v-if="errors.length"></p>
        <div class="alert alert-danger" role="alert" v-for="error in errors" :key="error">
          {{error}}
        </div>

        <modal :clickToClose= "false" name="my-first-modal" :width="400" :height="255">
          <div class="modal-content">
            <div class="modal-header">
              <h3>
                El centro fue creado con exito.
              </h3>
            </div>
            <div class ="modal-body">
              <p>Será redirigido a la página de inicio.</p>
            </div>
            <div class="modal-footer">
              <button type="submit" class="btn btn-success"  @click="cerrarModal" >
              Aceptar
            </button>
            </div>
          </div>
        </modal>


        <div class="form-group">
          <label>Nombre</label>
          <input class="form-control" type="text" v-model="nombre" required />
        </div>
        <div class="form-group">
          <label>Direccion</label>
          <input class="form-control" :value="address" readonly>
          <br>
          <div style="height: 550px;">
            <l-map
              ref="map"
              style="height: 90%; width: 100%"
              :zoom="zoom"
              :center="center"
              :point="point"
              :minZoom="minZoom"
              :maxZoom="maxZoom"
              :max-bounds="maxBounds"
              @update:center="centerUpdate"
              @update:zoom="zoomUpdate"
              @click="addPoint"
            >
              <l-tile-layer :url="url"></l-tile-layer>
              <l-geosearch :options="geoSearchOptions"></l-geosearch>
              <!-- Esto es un marcador -->
              <l-marker :lat-lng="point">
                <l-tooltip>{{ address }}</l-tooltip>
              </l-marker>
            </l-map>
          </div>
          <div class="form-group">
            <label>Telefono</label>
            <input
              class="form-control"
              type="text"
              name="phone"
              placeholder="xxx-xxx-xxxx"
              v-model="phone"
              required
            />
          </div>
        </div>
        <div class="form-group">
          <label>Hora de apertura</label>
          <input
            class="form-control"
            type="time"
            v-model="hsApertura"
            required
          />
        </div>
        <div class="form-group">
          <label>Hora de cierre</label>
          <input class="form-control" type="time" v-model="hsCierre" required />
        </div>
        <div class="form-group">
          <label>Municipio</label>
          <select v-model="muniElegido" value="" class="form-control" required>
            <option
              v-for="municipio in municipios"
              :key="municipio.id"
              :value="municipio.id"
              >{{ municipio.id }}-{{ municipio.name }}(Fase:{{
                municipio.phase
              }})
            </option>
          </select>
        </div>
        <div class="form-group">
          <label>Pagina web</label>
          <input
            class="form-control"
            type="text"
            placeholder="www.ejemplo.com"
            v-model="web"
          />
        </div>

        <div class="form-group">
          <label>Correo electronico</label>
          <input
            class="form-control"
            type="email"
            placeholder="ejemplo@ejemplo.com"
            v-model="email"
          />
        </div>

        <div class="form-group">
          <label>Tipo de centro</label>
          <select
            v-model="tipoCentroElegido"
            value=""
            class="form-control"
            required
          >
            <option
              v-for="tipoCentro in tiposCentros"
              :key="tipoCentro.nombre"
              :value="tipoCentro.nombre"
              >{{ tipoCentro.nombre }}
            </option>
          </select>
        </div>
        <vue-recaptcha sitekey="6Lft_QMaAAAAAHcAZZV3Uo8rQxg099tHU2GvZrwZ" @verify="evaluarCaptcha" :loadRecaptchaScript="true" ></vue-recaptcha>
        <br/>
        <button type="submit" class="btn btn-primary" @click="validateAndSend($event)">
          Agregar centro
        </button>
        <router-link class="btn btn-link" to="/">Volver a la página principal</router-link>
      </form>
    </section>
  </div>
</template>

<script lang="ts">
import { latLngBounds } from "leaflet"
import { LMap, LTileLayer, LTooltip, LMarker } from "vue2-leaflet";
import { OpenStreetMapProvider } from "leaflet-geosearch";
import LGeosearch from "vue2-leaflet-geosearch";
import axios from "axios";
import VueRecaptcha from 'vue-recaptcha';

export default {
  name: "Centros",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LTooltip,
    LGeosearch,
    VueRecaptcha
  },
  data() {
    return {
      zoom: 14,
      center: [-34.9187, -57.956],
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      point: [0, 0],
      geoSearchOptions: {
        provider: new OpenStreetMapProvider(),
        showMarker: false,
        autoClose: true
      },
      address: "",
      municipios: [],
      muniElegido: 0,
      tipoCentroElegido: "",
      tiposCentros: [],
      nombre: "",
      phone: "",
      hsApertura: "08:00",
      hsCierre: "16:00",
      web: "",
      email: "",
      matches: "",
      errors: [],
      minZoom: 6,
      maxZoom: 20,
      maxBounds: latLngBounds([
        [-32, -55],
        [-42, -65]
      ]),
      token: "",
      captcha: false
    };
  },
  mounted() {
    this.$refs.map.mapObject.on("geosearch/showlocation",this.onSearch);
  },
  created() {
    this.errors = [];
    this.cargarMunicipios()
      .then(res => res.json())
      .then(json => {
        this.municipios = json.data.Town;
      })
      .catch(e =>{
        this.errors.push("Hubo un error en la carga de municipios. Por favor, ingrese más tarde.");
      });
    this.cargarTiposCentros().then(res => {
        this.tiposCentros = res.data.tipos_de_centro;
      })
      .catch( e => {
        this.errors.push("Hubo un error en la carga de tipos de centro. Por favor, ingrese más tarde.");
      });
  },
  methods: {
    crearCentro() {
      const json = {
        nombre: this.nombre,
        direccion: this.address,
        telefono: this.phone,
        "hora_apertura": this.hsApertura,
        "hora_cierre": this.hsCierre,
        tipo: this.tipoCentroElegido,
        "municipio_id": this.muniElegido,
        latitud: this.point.lat,
        longitud: this.point.lng,
        web: this.web,
        email: this.email,
        token: this.token
      };
      const pagina = "https://admin-grupo69.proyecto2020.linti.unlp.edu.ar/centros";
      return axios
        .post(pagina, json);

    },
    zoomUpdate(zoom) {
      this.zoom = zoom;
    },
    centerUpdate(center) {
      this.center = center;
    },
    addPoint(point) {
      this.point = point.latlng;
      this.getAddress();
      this.mapClick = true;
    },
    onSearch(value) {
      const loc = value.location;
      this.point = { lat: loc.y, lng: loc.x };
      this.getAddress();
    },
    getAddress() {
      this.loading = true;
      const { lat, lng } = this.point;
      const pagina = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}`;
      axios.get(pagina).then(res => {
        this.address = res.data.display_name;
      })
      .catch( e => {
        this.errors.push("Hubo un error en la carga de dirección. Por favor, ingrese más tarde.");
      });

    },
    cargarMunicipios() {
      return  fetch("https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios")
    },
    cargarTiposCentros() {
      const pagina = `https://admin-grupo69.proyecto2020.linti.unlp.edu.ar/tipos_de_centro`;
      return axios.get(pagina);
    },
    validateAndSend(event) {
      this.errors = [];
      if (!this.validateTel()) {
        this.errors.push("Número de teléfono inválido");
      }
      if (!this.validateWeb()) {
        this.errors.push("Pagina web inválida");
      }
      if (!this.validateName()) {
        this.errors.push("Debe ingresar un nombre válido");
      }
      if(this.address === "" && (!this.mapClick)){
        this.errors.push("Debe seleccionar un punto en el mapa");
      }
      if(!this.captcha){
        this.errors.push("Debe realizar el captcha");
      }
      if (this.errors.length === 0) {
        this.crearCentro()
          .then(response => {
            this.$modal.show('my-first-modal');
          }).catch(e => {
            this.errors.push(e.response.data.error);
          });
      }
      event.preventDefault();
    },
    validateTel() {
      //eslint-disable-next-line
      const regex = /^(\d{3})[-]?(\d{3})[-]?(\d{4})$/;
      const found = regex.test(this.phone);
      return found;
    },
    validateWeb() {
      if (this.web) {
        //eslint-disable-next-line
        const regex = /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)/;
        const found = regex.test(this.web);
        return found;
      }
      return true;
    },
    validateName(){
      return this.nombre.trim() != "";
    },
    cerrarModal () {
      this.$modal.hide('my-first-modal');
      this.$router.push("/");
    },
    evaluarCaptcha: function ( recaptchaToken ) {
      this.token = recaptchaToken;
      this.captcha = true;
    }
  }
};
</script>
