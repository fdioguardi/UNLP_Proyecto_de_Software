<template>
  <main role="main">
    <h1 class="display-4 fw-normal">Estadisticas</h1>
    <div class="position-relative overflow-hidden p-3 p-md-5 m-md-3 text-center bg-light">
      <div class="col">
        <h2 class="display-4 fw-normal">Centros populares</h2>
        <Bar/>
      </div>
      <div class="product-device shadow-sm d-none d-md-block"></div>
      <div class="product-device product-device-2 shadow-sm d-none d-md-block"></div>
    </div>
    <div class="row">
      <div class="bg-light text-center col">
        <div class="my-6 py-6">
          <h2 class="display-5">Tipos de centros</h2>
          <Ring/>
        </div>
      </div>
      <div class="bg-light text-center col">
        <div class="my-3 p-3">
          <h2 class="display-5">Distribución por municipios</h2>
          <Histogram/>
        </div>
      </div>
    </div> 
  </main>
</template>

<script >
import { Component, Vue } from "vue-property-decorator";
import Ring from "@/components/Ring.vue"; // @ is an alias to /sr
import Histogram from "@/components/Histogram.vue";
import Bar from "@/components/Bar.vue";

export default {
  name: "Statistics",
  components: {
    Ring,
    Histogram,
    Bar
  }
}
</script>
