<template>
  <div id="app">
    <header>
      <nav>
        <div class="display-4">Donaciones COVID-19</div>
        <router-link to="/">Inicio</router-link> |
        <router-link to="/mapa">Ver mapa</router-link> |
        <router-link to="/turno">Sacar turno</router-link> |
        <router-link to="/centros">Nuevo centro</router-link> |
        <router-link to="/estadisticas">Estadísticas</router-link>
      </nav>
      <hr class="my-4">
    </header>
    <router-view />
    <footer class="container mw-100">
      <hr class="my-4">
      <p>© Gobierno de la Provincia de Buenos Aires - 2020</p>
    </footer>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #252525;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #383838b7;
}

nav a.router-link-exact-active {
  color: #1f1f1fef;
}

header {
  background-color: #e3f2fd;
}
</style>
