import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue")
  },
  {
    path: "/mapa",
    name: "Mapa",
    component: () => import("../views/Mapa.vue")
  },
  {
    path: "/centros",
    name: "Centros",
    component: () =>
      import(/* */"../views/Centros.vue")
  },
  {
    path: "/turno",
    name: "Turno",
    component: () =>
      import("../views/Turns.vue")
  },
  {
    path: "/estadisticas",
    name: "Estadísticas",
    component: () =>
      import("../views/Statistics.vue")
  }
];

const router = new VueRouter({
  routes
});

export default router;
