<template>
  <div>
    <div v-show="errorInApi" class="alert alert-warning alert-dismissible fade show" role="alert">
      Hubo un problema al cargar la estadística de Tipos de Centro, intente más tarde.
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
    <ve-ring v-show="!errorInApi" :data="chartData" :loading="loading" :settings="chartSettings"></ve-ring>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import VeRing from 'v-charts/lib/ring.common';
import axios from "axios";

Vue.component(VeRing.name, VeRing);

@Component
export default class Ring extends Vue {
  @Prop() private errorInApi!: boolean;
  @Prop() private chartSettings!: object;
  @Prop() private chartData!: object;

  data () {
    this.chartSettings = {
      selectedMode: 'single',
    }
    this.chartData = {
      columns: [ 'Nombre', 'Cantidad', ],
      rows: []
    }

    this.errorInApi = false;

    return {

    }
  }
  created() {
    const pagina = `https://admin-grupo69.proyecto2020.linti.unlp.edu.ar/tipos_de_centro`
    axios.get(pagina)
      .then(response => {
        this.chartData.rows = response.data.tipos_de_centro.map(
          row => {
            return {
              "Nombre": row.nombre,
              "Cantidad": row.cant_centros,
            };
          }
        );
      })
      .catch(e => { this.errorInApi = true; });
  }
}
</script>

<style scoped>

.card {
  margin: 0 auto;
  float: none;
  margin-bottom: 10px;
  width: 18rem;
}

h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
