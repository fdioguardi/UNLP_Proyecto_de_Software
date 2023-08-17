<template>
    <nav class="navbar navbar-expand-lg navbar-light" id="navbar" style="background-color: #e3f2fd;">
      <a class="navbar-brand" href="#">Donar</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav mr-auto"> 
          <li class="nav-item">
            <a class="nav-link" href="#">Boton</a>
          </li>
        </ul>
        <ul class="navbar-nav ml-auto"> 
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <p>hola</p>
            </a>
            <div class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdownMenuLink">
              <a class="dropdown-item" href="#">Perfil</a>
            </div>
          </li>
        </ul>
      </div>
    </nav>
</template>
<script>
    import "bootstrap";
    import "bootstrap/dist/css/bootstrap.min.css";
    import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class Layout extends Vue {
}

</script>