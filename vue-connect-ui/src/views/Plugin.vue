<template>
  <div>
    <div class="box notification is-primary">
      <div class="columns">
        <div class="column is-1">
          <p class="title">
            {{ $route.name }}
          </p>
        </div>
        <div class="column is-8 is-offset-1">
        </div>
        <div class="column is-1 is-offset-1">
          <button
            v-on:click="reload()"
            v-bind:class="[isLoading != `` ? `is-loading` : ``]"
            class="button"
          >
            <font-awesome-icon icon="sync-alt"></font-awesome-icon>
          </button>
        </div>
      </div>
    </div>

    <div class="box">
      <error-message :error="errors"></error-message>

      <table v-if="data.length > 0" class="table is-hoverable">
        <thead>
          <tr>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="plugin in data" :key="plugin.class">
            <td>
              <b>{{ plugin.name }}</b>
              <ul>
                <li>Class: {{ plugin.class }}</li>
                <li>Type: {{ plugin.type }}</li>
                <li>Version: {{ plugin.version }}</li>
              </ul>
            </td>
            <td>
              <a
                class="button is-primary is-small"
                v-on:click="newConnector(plugin.class, plugin.type)"
                ><font-awesome-icon icon="plus-circle"></font-awesome-icon
                ><span class="pl-1">New connector</span></a
              >
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
<script>
import connect from "../common/connect";
import errorHandler from "../common/error";
import ErrorMessage from "../components/ErrorMessage.vue";

function loadData() {
  this.isLoading = "plugins";
  connect
    .getPlugins()
    .then((response) => {
      // JSON responses are automatically parsed.
      this.data = response.data;
      this.isLoading = "";
    })
    .catch((e) => {
      this.errors = errorHandler.transform(e);
      this.isLoading = "";
    });
}

export default {
  components: { ErrorMessage },
  data() {
    return {
      data: [],
      errors: null,
      isLoading: "",
    };
  },

  created() {
    loadData.bind(this)();
  },

  methods: {
    newConnector: function(pluginClass, pluginType) {
      this.$router.push("/new/" + pluginClass + "/" + pluginType);
    },
    reload: function() {
      loadData.bind(this)();
    },
  },
};
</script>
