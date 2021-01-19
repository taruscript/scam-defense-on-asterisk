<template>
  <div class="small">
    <line-chart :chart-data="datacollection"></line-chart>
    <button @click="fillData()">Randomize</button>
  </div>
</template>

<script>
import LineChart from './LineChart.js'
  export default {
    components: {
      LineChart
    },
    data () {
      return {
        datacollection: null,
        scores: [],
        labels: []
      }
    },
    mounted () {
      this.fillData()
    },
    methods: {
        fillData () {
            this.createLabels()
            this.appendScores()
            this.datacollection = {
            labels: this.labels,
            datasets: [
                {
                label: 'Data One',
                backgroundColor: '#f87979',
                data: this.scores
                }
            ],
            }
        },      
        getRandomInt () {
            return Math.floor(Math.random() * (50 - 5 + 1)) + 5
            // return 1
        },
        appendScores() {
            this.scores.push(this.getRandomInt())
        },
        createLabels() {
            this.labels.push(this.scores.length)
        } 
    }
  }
</script>


<style>
  .small {
    max-width: 600px;
    margin:  150px auto;
  }
</style>
