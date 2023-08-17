<template>
  <div class="card col-md-3">
    <div class="card-body">
      <h2 class="card-title">{{ title }}</h2>
      <p class="card-text">{{ msg }}</p>
      <p>
      <router-link class="btn btn-info" style="color: #ffffff;" :to="btnLink">{{
        btnMsg
        }}</router-link>
      </p>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class EmbeddedCard extends Vue {
  @Prop() private title!: string;
  @Prop() private msg!: string;
  @Prop() private btnMsg!: string;
  @Prop() private btnLink!: string;
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
