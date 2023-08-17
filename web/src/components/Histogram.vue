<template>
    <div>
        <div v-show="errorInApi" class="alert alert-warning alert-dismissible fade show" role="alert">
          Hubo un problema al cargar la estadística de Distribución por municipios, intente más tarde.
          <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <ve-histogram v-show="!errorInApi" :data="chartData" :settings="chartSettings"></ve-histogram>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import VeHistogram from 'v-charts/lib/histogram.common';
import axios from "axios";

Vue.component(VeHistogram.name, VeHistogram);

export default{
    name: "Histogram",
    components: {
      VeHistogram
    },
    data: function () {
          return {
            chartSettings: {
              metrics: ['Centros', 'Turnos'],
              stack: { 'Info': ['Centros', 'Turnos'] }
            },
            chartData: {
              columns: ['Municipio', 'Centros', 'Turnos'],
              rows: []
            },
            errorInApi: false
      }
    },
    created() {
      this.getData();
    },
    methods: {
      getData() {
        const pagina = "https://admin-grupo69.proyecto2020.linti.unlp.edu.ar/municipios";
        axios.get(pagina)
          .then(response => {
            this.chartData.rows = response.data.Municipios;
            this.renameTowns();
          })
          .catch(e => {this.errorInApi = true;} );
      },
      renameTowns() {
        const pagina = "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios";
        axios.get(pagina)
          .then(response => {
            this.replaceTowns(response.data.data.Town);
          })
          .catch(e => {this.errorInApi = true;} );
      },
      replaceTowns(towns) {
        this.chartData.rows.forEach(element => {
          const aux = element['Municipio'];
          element['Municipio'] = towns[aux].name;
        });
      }
    }
}
</script>
