<template>
  <div class="demo">
    <div class="score">
      <line-chart :chart-data="datacollection"></line-chart>
      <button @click="fillData()">Randomize</button>
    </div>
  </div>
</template>

<script>
import LineChart from './LineChart.js'
import axios from 'axios'
import gsap from 'gsap'

  export default {
    components: {
      LineChart
    },
    data () {
      return {
        datacollection: null,
        scores: [],
        labels: [],
        words: [],
        count: 0,
        before_score: 0
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
                const results = res.data["results"]

                this.scores.push(total_score)
                if (this.before_score != total_score) {
                  this.before_score = total_score
                  for (const result in results) {
                    const target_keyword = results[result]["target_keyword"]
                    this.words.push(target_keyword)
                  }
                }
            })
            this.renderMoveText()
        },
        async fillData () {
          for(;;){
            await this.fetchGetResult()
            // this.renderMoveText()
            this.createLabels()

            this.datacollection = {
              labels: this.labels,
              datasets: [
                  {
                  label: '詐欺脅威度',
                  backgroundColor: '#f87979',
                  data: this.scores
                  }
              ]
            }
            // this.sleep(5000)
          }
        }, 
        createLabels() {
            this.labels.push(this.scores.length)
        },
        sleep(waitMsec) {
            var startMsec = new Date();
            // 指定ミリ秒間だけループさせる（CPUは常にビジー状態）
            while (new Date() - startMsec < waitMsec);
        },
        async createText(word) {
          let div_text = document.createElement('div');
          // div_text.class="move_text";
          div_text.id="text"+this.count; //アニメーション処理で対象の指定に必要なidを設定
          this.count ++
          div_text.style.position = 'fixed';
          div_text.style.whiteSpace = 'nowrap';
          div_text.style.left = (document.documentElement.clientWidth) + 'px'; 
          var random = Math.round( Math.random()*document.documentElement.clientHeight );
          div_text.style.top = random + 'px'; 
          div_text.appendChild(document.createTextNode(word));
          document.body.appendChild(div_text); 

          //ライブラリを用いたテキスト移動のアニメーション： durationはアニメーションの時間、
          //        横方向の移動距離は「画面の横幅＋画面を流れるテキストの要素の横幅」、移動中に次の削除処理がされないようawait
          await gsap.to("#"+div_text.id, {duration: 50, x: -1*(document.documentElement.clientWidth+div_text.clientWidth)});

          div_text.parentNode.removeChild(div_text); //画面上の移動終了後に削除
        },
        async renderMoveText(){
            for (const word in this.words) {
              const target_keyword = this.words[word]
              await this.createText(target_keyword)
          }
          // 関数実行の度に文字流しの部分を初期化する
          this.words = []
        }
    }
  }
</script>


<style>
  .score {
    max-width: 600px;
    margin:  150px auto;
    /* width: 50%;
    height: 100%; */
  }
  .move_text {
    font-size: 5%;
  }
</style>
