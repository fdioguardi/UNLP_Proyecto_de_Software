<template>
  <div class="Turns">
    <div class="container border border-light p-5 text-left">
      <h1>Nuevo turno</h1>
      <br/>
      <div v-show="errors.length">
        <div class="alert alert-danger" role="alert" v-for="error in errors" :key="error">{{error}}</div>
      </div>
      <modal :clickToClose= "false" name="my-first-modal" :width="400" :height="255">
        <div class="modal-content">
          <div class="modal-header">
            <h3>
              El turno fue creado con exito.
            </h3>
          </div>
          <div class ="modal-body">
            <p>Será redirigido a la página de inicio.</p>
          </div>
          <div class="modal-footer">
            <button type="submit" class="btn btn-success"  @click="cerrarModal" >
              Aceptar
            </button>
          </div>
        </div>
      </modal>
      <form>
        <div class="form-group">
          <label>Centro</label>
          <select
            v-model="id"
            @change="centerSelected()"
            class="form-control"
            required
          >
            <option v-for="centro in centros"  :key="centro.id" :value="centro.id">
            {{ centro.nombre }}</option></select
          >
        </div>
        <div v-show="centroElegido">
          <div class="form-group">
            <label>Email</label>
            <input
              v-model="email"
              type="email"
              class="form-control"
              placeholder="ejemplo@ejemplo.com"
              required
            />
          </div>
          <div class="form-group">
            <label>Telefono</label>
            <input
              v-model="tel"
              type="tel"
              class="form-control"
              placeholder="xxx-xxx-xxxx"
              required
            />
          </div>
          <div class="form-group">
            <label>Dia</label>
            <input
              type="date"
              class="form-control"
              v-model="fecha"
              :min="hoy"
              required
              @change="daySelected()"
            />
          </div>
          <div v-show="elegido" class="form-group">
            <label>Horario</label>
            <select
              v-model="horario"
              @change="onChange()"
              class="form-control"
              required
            >
              <option v-for="turno in turnos" :key="turno.turno_id" >{{ turno.hora_inicio }} a {{ turno.hora_fin }}</option>
            </select>
          </div>     
        </div>
        <button @click="validateAndSend($event)" type="submit" class="btn btn-primary">Cargar</button>
        <router-link class="btn btn-link" to="/">Volver</router-link>
      </form>
    </div>
  </div>
</template>
<script>
import axios from "axios";
export default {
  name: "Turns",
  data() {
    return {
      errors: [],
      id: "",
      fecha: "",
      centroElegido: false,
      elegido: false,
      email: "",
      turnos: [],
      centros: [],
      inicio: "",
      fin: "",
      tel: "",
      mensaje: "",
      horario: "",
      hoy: "",
      hayError: false
    };
  },
  mounted() {
    this.getDate();
    this.getCenters();
  },
  methods: {
    getDate: function() {
      const now = new Date();
      this.hoy = now.getFullYear() + "-" + (now.getMonth()+1) + "-" + now.getDate();
    },
    getCenters: function() {
      axios
        .get("https://admin-grupo69.proyecto2020.linti.unlp.edu.ar/centros?all=True")
        .then(response => {
          this.centros = response.data.centros;
        })
        .catch(e => {
          console.log(e);
        });
    },
    requestSchedule: function() {
      axios
        .get(
          "https://admin-grupo69.proyecto2020.linti.unlp.edu.ar/centros/" +
            this.id +
            "/turnos_disponibles/?fecha=" +
            this.fecha
        )
        .then(response => {
          this.turnos = response.data.turnos;
        })
        .catch(e => {
          console.log(e);
        });
    },
    createTurn: function() {
      const json = {
        "centro_id": this.id,
        "email_donante": this.email,
        "telefono_donante": this.tel,
        "hora_inicio": this.inicio,
        "hora_fin": this.fin,
        fecha: this.fecha
      };
      return axios.post(
        "https://admin-grupo69.proyecto2020.linti.unlp.edu.ar/centros/" + this.id + "/reserva", json)
    },
    onChange: function() {
      const temp = this.horario.split(" a ");
      this.inicio = temp[0];
      this.fin = temp[1];
    },
    centerSelected: function() {
      this.centroElegido = true;
    },
    daySelected: function() {
      this.requestSchedule();
      this.elegido = true;
    },
    validateAndSend: function(e) {
      this.errors = [];
      this.hayError = false;
      this.validate();

      if(!this.hayError)
      {
        this.errors = [];
        this.createTurn()
        .then(response => {
          this.$modal.show('my-first-modal');
        })
        .catch(e => {
          console.log(e.response.data.error);
          this.errors.push(e.response.data.error);
        });
      }
      e.preventDefault();
    },
    validate: function() {
      const regex = /^(\d{3})[-]?(\d{3})[-]?(\d{4})$/;
      const emailRegex = /^\S+@\S+\.\S+$/;
      const emailCheck = emailRegex.test(this.email);
      const found = regex.test(this.tel);
      if(!found)
      {
        this.errors.push("El formato del telefono no es válido");
        this.hayError = true;
      }
      if(!emailCheck)
      {
        this.errors.push("El formato del email no es válido");
        this.hayError = true;
      }
    },
    cerrarModal () {
        this.$modal.hide('my-first-modal');
        this.$router.push("/");
    }
  }
};
</script>
