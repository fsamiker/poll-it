<template>
<div class="poll" v-show="!!pollData.id">
  <section class="hero is-primary">
    <div class="hero-body">
      <div class="container has-text-centered">
        <h1 class="title is-3 mb-6">Poll #{{ pollData.id }}</h1>
        <h2 class="subtitle is-1"> {{ pollData.title }} </h2>
      </div>
    </div>
    <div class="hero-foot">
      <div class="container has-text-centered">
        <p>Created by: <a class="has-text-white" :href="ownerLink" >{{ pollData.created_by.username }}</a></p>
      </div>
    </div>
  </section>
  <section class="section vote pb-0">
    <div class="container">
    <div class="columns">
        <div class="column">
          <div class="container box">
            <p class="title">Description</p>
            <p class="subtitle is-6 mt-3">{{ pollData.description}}</p>
          </div>
        </div>
        <div class="column">
          <div class="container box has-text-centered">
            <Timer v-show="!!pollData.id" :endTime="expireTime" @expired="endPoll" class="title" ></Timer>
          </div>
        </div>
      </div>
    </div>
  </section>
  <section class="section stats pb-0">
    <div class="container box">
      <p class="title has-text-centered"> Statistics</p>
      <div class="columns is-vcentered">
        <div class="column">
          <PollChart :chartData="pollData.chart_values" :key="pollData.id"></PollChart>
        </div>
        <div class="column">
          <div class="mb-5" v-for="option in pollData.options" :key="option.id">
            <p class="pl-5" > {{ option.body }} </p>
            <progress class="progress" :max="pollData.total_votes" :value="option.vote_count"></progress>
          </div>
        </div>
      </div>
    </div>
  </section>
</div>
</template>

<script>
import { fetchPoll } from '@/api'
import Timer from '@/components/Timer'
import PollChart from '@/components/PollChart'
import moment from 'moment'

export default {
  name: 'PollDetailed',
  components: {
    Timer,
    PollChart
  },
  data: function(){
    return {
      'pollData': {
        id: null,
        title: '',
        created_by: ''
      }
    }
  },
  created: function() {
    this.getPollData();
    console.log(this.$route.name)
  },
  computed: {
    pollId: function() {
      return this.$route.params.id
    },
    expireTime: function() {
      return moment(this.pollData.expires_at)
    },
    ownerLink: function() {
      return '/user/' + this.pollData.created_by.id
    }
  },
  methods: {
    getPollData: function() {
      fetchPoll(this.pollId)
      .then(response => response.json())
      .then(data => {
        this.pollData = data;
      });
    },
    endPoll: function() {
          this.pollData.expired = true
    }
  }
};
</script>

<style scoped>
</style>