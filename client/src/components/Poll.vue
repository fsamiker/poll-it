<template>
    <div class="column is-one-quarter">
        <article class="box poll">
            <div class="content">
                <p class="title is-4 has-text-centered"><a class="has-text-black" :href="pollLink">{{ pollData.title }}</a></p>
                <p class="subtitle is-6 has-text-centered mb-2"><a class="has-text-black" :href="ownerLink">{{ pollData.created_by.username }}</a></p>
                <hr>
                <Timer :endTime="expireTime" @expired="endPoll" class="has-text-centered mt-3"></Timer>
                <div class="container poll-content mt-4">
                    <figure class="image pt-0 my-0">
                        <PollChart :chartData="pollData.chart_values" v-show="voted || pollData.expired" :key="voted"></PollChart>
                    </figure>
                    <Options v-show="!voted && !pollData.expired" :optionList="pollData.options" :pollId="pollData.id" :expired="pollData.expired"></Options>
                </div>
            </div>
            <div class="level is-mobile">
                <div class="level-right">
                    <div class="level-item">
                        <DeletePollButton class="level-item is-small" v-show="isOwner" :pollId="pollData.id" @remove="$emit('remove')"></DeletePollButton>
                    </div>
                </div>
            </div>
        </article>
    </div>
</template>

<script>
import Options from './Options'
import DeletePollButton from './DeletePollButton'
import Timer from './Timer'
import moment from 'moment'
import PollChart from './PollChart'

export default {
  name: 'Poll',
  props: ['pollData'],
  data: function() {
      return {
          selected_id: null
      }
  },
  components: {
      Options,
      DeletePollButton,
      Timer,
      PollChart
  },
  computed: {
      voted: function() {
          if (Object.keys(this.$store.state.votedPolls).includes(this.pollData.id.toString())) {
              return true;
          }
          return false;
      },
      expireTime: function() {
          return moment(this.pollData.expires_at)
      },
      ownerLink: function() {
          return '/user/' + this.pollData.created_by.id
      },
      pollLink: function() {
          return '/poll/' + this.pollData.id
      },
      isOwner: function() {
          if(!this.$store.state.user) {
              return false
          }
          else if (this.$store.state.user.id === this.pollData.created_by.id){
              return true
          }
          return false
      }
  },
  methods: {
      endPoll: function() {
          this.pollData.expired = true
      }
    }
};
</script>

<style scoped>
.poll {
    height: 375px;
}

.poll-content{
    height: 175px;
    width: 250px;
}

hr {
    margin: 0;
}
</style>