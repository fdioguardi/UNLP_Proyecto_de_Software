<template>
  <div>
    <div v-show="errorInApi" class="alert alert-warning alert-dismissible fade show" role="alert">
      Hubo un problema al cargar la estadística de Centros más populares, intente más tarde.
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
  <ve-bar v-show="!errorInApi" :data="chartData" :settings="chartSettings"></ve-bar>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import VeBar from 'v-charts/lib/bar.common';
import axios from "axios";

Vue.component(VeBar.name, VeBar);

@Component
export default class Bar extends Vue{
    @Prop() private errorInApi!: boolean;
    @Prop() private chartSettings!: object;
    @Prop() private chartData!: object;

    data() {
        this.chartSettings = {
                metrics: ['Turnos'],
                dataOrder: {
                    label: 'Turnos',
                    order: 'desc'
                }
            }
        this.chartData = {
            columns: ['Nombre', 'Turnos'],
            rows: []
        }
        this.errorInApi = false;
        return {

        }
    }
    created() {
      const pagina = "https://admin-grupo69.proyecto2020.linti.unlp.edu.ar/turnos_por_centro";
        axios.get(pagina)
          .then(response => {
            this.chartData.rows = response.data.Centros;
          })
          .catch(e => { this.errorInApi = true; } );
    }
  }
</script>
