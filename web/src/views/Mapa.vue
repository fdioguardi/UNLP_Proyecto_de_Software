<template>
  <div class="container mt-4">
      <h1>Mapa de centros de ayuda social</h1>
      <p>Presione sobre un marcador para ver información del centro deseado</p>
      <div style="height: 500px;">
        <l-map
          style="height: 90%; width: 100%"
          :zoom="zoom"
          :center="center"
          :minZoom="minZoom"
          :maxZoom="maxZoom"
          :max-bounds="maxBounds"
          @update:zoom="zoomUpdate"
          @update:center="centerUpdate"
        >
          <l-tile-layer :url="url"></l-tile-layer>
          <l-marker v-for="centro in centros" :key="centro.direccion" :lat-lng="[centro.latitud,centro.longitud]">
            <l-tooltip class="titulo"> {{ centro.nombre }} </l-tooltip>
            <l-popup>
              <p class="titulo "> {{ centro.nombre }} </p>
              <ul>
                <li> Dirección: {{ centro.direccion }} </li>
                <li> Donaciones: {{ centro.center_type }} </li>
                <li> Horario: {{ centro.hora_apertura }} - {{ centro.hora_cierre }} </li>
                <li> Teléfono: {{ centro.telefono }} </li>
              </ul>
            </l-popup>
          </l-marker>
        </l-map>
      </div>
  </div>
</template>

<style scoped>
.titulo {
  text-align:center;
  font-weight: bold;
  font-size: larger;
}
li {
  margin: 0px;
  padding: 0px;
}
ul {
    margin: 0px;
    padding: 0px;
}
</style>

<script lang="ts">
import { latLngBounds } from "leaflet"
import { LMap, LTileLayer, LMarker, LPopup, LTooltip } from "vue2-leaflet";
import axios from "axios";

export default {
  name: "Mapa",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
    LTooltip
  },
  data() {
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      center: [-34.9187, -57.956],
      zoom: 12,
      minZoom: 6,
      maxZoom: 20,
      maxBounds: latLngBounds([
        [-32, -55],
        [-42, -65]
      ]),
      centros: []
    };
  },
  mounted() {
    this.getCentros();
  },
  methods: {
    zoomUpdate(zoom) {
      this.zoom = zoom;
    },
    centerUpdate(center) {
      this.center = center;
    },
    getCentros() {
      const pagina = "https://admin-grupo69.proyecto2020.linti.unlp.edu.ar/centros?all=True";
      axios
        .get(pagina)
        .then(respuesta => {
          this.centros = respuesta.data.centros;
        })
        .catch(e => {
          console.log(e);
        });
    }
  }
};
</script>
