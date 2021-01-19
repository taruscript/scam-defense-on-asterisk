<template>
  <div class="small">
    <line-chart :chart-data="datacollection"></line-chart>
    <button @click="fillData()">Randomize</button>
  </div>
</template>

<script>
import LineChart from './LineChart.js'
import axios from 'axios'

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

        async fetchGetResult(){
            await axios.get("/current_score").then(res => {
                console.log(res.data)
                const total_score = res.data["total_score"] 
                this.scores.push(total_score)
            })
        }
        ,
        async fillData () {
            for(;;){
            this.sleep(5000)
            this.createLabels()
            // this.appendScores()
            await this.fetchGetResult()
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
        },
        sleep(waitMsec) {
            var startMsec = new Date();
            // 指定ミリ秒間だけループさせる（CPUは常にビジー状態）
            while (new Date() - startMsec < waitMsec);
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
