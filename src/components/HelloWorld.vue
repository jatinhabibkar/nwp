<template>
  <div class="hello">
 <input id="change" type="number" maxlength="2" size="2" placeholder="enter No" v-model="thep">

    <div class="row">
      <form class="col s12">
        
        <div class="row">
          <div @change="helpertext" >
            <span  v-for="(i,ii) in helpertext" :key="ii" class="chip" v-on:click="pasteit(i)" style="cursor:pointer"> &nbsp; {{i}} &nbsp;</span>
            </div>
          <div class="input-field col s12">

            <textarea  id="mysize" class="materialize-textarea" cols=100 placeholder="textarea" v-model="text" ></textarea>
            
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
      text:"That which does not kill us makes us stronger. To live is to suffer, to survive is to find some meaning in the suffering.",
      thep:3,
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
    },
    pasteit(i){
      console.log(i)
      this.text+=i
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
        console.log(this.thep)

        if(this.text.length>40){
                let mythis=this;
                mythis.socket.emit("filter change",{
                  filter:mythis.text,
                  thep:mythis.thep
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
#change{
  width: 100px;
  float: right;
  height: 40px;
  margin-top: 10px;
  overflow: hidden;
}

</style>

