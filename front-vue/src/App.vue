<template>
    <div class="field">

        <label class="label">Label</label>

        <form>

        <div class="control">

            <input class="input" type="text" placeholder="Enter subject code" name="code">

            <button class="button is-primary" @click="hideModal">Submit</button>


        </div>

        </form>
        <p class="help">This is a help text</p>

    </div>
</template>

<script>

import axios from 'axios';

export default {
  name: 'app',

  data: () => ({

  }),

  methods: {
      hideModal() {
          axios.get(`http://localhost:3000/axios`).then(response => console.log(response))

      }
  },


  }




</script>

<style>

</style>
