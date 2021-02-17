<template>
  <div class="hello">
      
    <div class="row">
      <form class="col s12">
   
        <div class="row">
          <div class="input-field col s12">
            <textarea  id="mysize" class="materialize-textarea" cols=100 placeholder="textarea" v-model="text" ></textarea>
            <div @change="helpertext" >
            <span  v-for="(i,ii) in helpertext" :key="ii" class="chip"> {{i}} &nbsp;</span>
            </div>
          </div>
        </div>
      </form>
    </div>

  </div>
</template>

<script>
import io from 'socket.io-client';

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data(){
    return{
      text:"The JSON format is syntactically identical to the code for creating JavaScript objects.Because of this similarity, a JavaScript program can easily convert JSON data into native JavaScript objects.",
      helpertext:null,
      socket:io('http://localhost:5000',{
        transport:[
          'websocket'
        ]
      })
    }
  },

  methods:{
    input(){
      console.log(this.text)
    }
  },
  mounted(){
    this.socket.on('connect', function(){
      console.log("connected");
    });  
    let mythis=this
    this.socket.on('event',function(socket) {
      try{
        // console.log(socket.prediction)
        mythis.helpertext=socket.prediction

      }catch(err)
      {
          console.log(err)
      } 
    })
  },
  watch:{
    text :function(){
        console.log(this.text)

        if(this.text.length>40){
                let mythis=this;
                mythis.socket.emit("filter change",{
                  filter:mythis.text
          })
        }
    }
  }
}
</script>

<style scoped>
#mysize{
  height:50rem !important
}
</style>

