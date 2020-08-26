<template>
    <div class="time-left">
        <p v-show="secondsLeft > 0" class="mb-0">{{ display }}</p>
        <button class="button is-primary is-outlined is-static is-small" v-show="secondsLeft <= 0">Poll Closed</button>
    </div>
</template>

<script>
import moment from 'moment'

export default {
  name: 'Timer',
  props: ['endTime'],
  data: function() {
      return {
          secondsLeft: 0,
      }
  },
  created: function() {
      this.secondsLeft = this.endTime.diff(moment(), 'seconds')
      setInterval(()=> this.secondsLeft = this.secondsLeft-1, 1000)
  },
  watch: {
      secondsLeft: function() {
          if (this.secondsLeft < 0) {
              this.$emit('expired')
          }
      }
  },
  computed: {
      seconds: function() {
          return this.secondsLeft % 60
      },
      hours: function() {
          return Math.floor(this.secondsLeft/3600);
      },
      minutes: function() {
          return Math.floor(this.secondsLeft%3600/60);
      },
      display: function() {
          if (this.secondsLeft > 0) {
              return `${this.prependZero(this.hours)} : ${this.prependZero(this.minutes)} : ${this.prependZero(this.seconds)}`
          }
          return 'Expired : '+ moment(this.endTime).format('DD-MM-YYYY hh:mm:ss')
      }
  },
  methods: {
      prependZero: function(integer) {
          if (integer < 10) {
              return `0${integer}`
          }
          return integer.toString()
      }
  }
};
</script>

<style scoped>
</style>