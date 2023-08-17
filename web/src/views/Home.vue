<template>
  <main role="main">
    <!-- Main jumbotron for a primary marketing message or call to action -->
    <div style="background-color: #ffffff;" class="jumbotron">
      <div class="container">
        <h2 class="display-4">¡Dona de todo!</h2>
        <p>
          En épocas de COVID-19, es imperativo mantener las medidas de seguridad
          recomendadas por la OMS. Por eso, si querés donar para ayudar a las personas
          que más lo necesitan, hacelo con cuidado. Pasemos esta pandemia entre todos.
        </p>
        <p>
          <router-link class="btn btn-primary btn-lg" to="/mapa"
            >Encontrá tu centro más cercano</router-link
          >
        </p>
      </div>
    </div>
    <hr>

    <div class="container">
      <!-- Example row of columns -->
      <div class="row">
        <EmbeddedCard
          title="Turnos"
          msg="Sacá un turno para donar con seguridad en el centro de donación que elijas,
                respetando todas las medidas recomendadas por la OMS y el Ministerio de salud."
          btnMsg="Sacar un turno"
          btnLink="/turno"
        />
        <EmbeddedCard
          title="Nuevo centro"
          msg="¿Conoces un centro de donaciones que no figura en la página? Agregalo para permitir
                que más gente done cerca de su casa y así poder ayudarnos entre todos."
          btnMsg="Crear un centro"
          btnLink="/centros"
        />
        <EmbeddedCard
          title="Estadísticas"
          msg="Mirá estadísticas sobre los tipos de centros de la provincia, y otros datos interesantes
                que hemos recopilado sobre los centros de donaciones."
          btnMsg="Ir a estadísticas"
          btnLink="/estadisticas"
        />
      </div>
    </div>
  </main>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import EmbeddedCard from "@/components/EmbeddedCard.vue"; // @ is an alias to /sr
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
@Component({
  components: {
    EmbeddedCard
  }
})
export default class Home extends Vue {}
</script>
