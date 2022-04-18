<template>
  <q-page class="flex flex-center q-mx-lg">
    <q-timeline :layout="layout" color="secondary" class="q-my-xl">
      <q-timeline-entry heading>
        Temperature and Gas Monitoring
      </q-timeline-entry>
          <q-timeline-entry title="GAS" side="right" >
          <p
            class="text-weight-medium"
            :style="{ color: this.gas===0 ? 'red' : 'black' }"
          >
            <q-icon
              name="img:https://images.vexels.com/media/users/3/217992/isolated/preview/2cd4b4156f5a4e44235c3abe0e594f0e-fume-smoking-icon-by-vexels.png"
              size="30px"
            />
             &nbsp;  &nbsp; Gas Status: &nbsp; {{ this.gas===0 ? 'DETECTED' : 'NOT DETECTED' }}
          </p>
          <p
            class="text-weight-medium"
            :style="{ color: this.gas===0 ? 'red' : 'black' }"
          >
            <q-icon
              name="img:https://cdn-icons-png.flaticon.com/512/1100/1100349.png"
              size="30px"
            />
            &nbsp;  &nbsp;  Alarm status: &nbsp; {{ this.gas===0 ? 'BUZZING' : 'NOT BUZZING' }}
          </p>
          </q-timeline-entry>


          <q-timeline-entry title="TEMPERATURE" side="left" >
          <p
            class="text-weight-medium"
            :style="{ color: this.temp>=this.threshold ? 'red' : 'black' }"
          >
            <q-icon
              name="img:https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRTByhvLtZ0ine5AP2ZBmUOCGWojaBcjOogmg&usqp=CAU"
              size="30px"
            />
             &nbsp;  &nbsp; Temperature Reading: &nbsp; {{ this.temp }}
          </p>
          <p
            class="text-weight-medium"
            :style="{ color: this.temp>=this.threshold ? 'red' : 'black' }"
          >
            <q-icon
              name="img:https://cdn-icons-png.flaticon.com/512/556/556878.png"
              size="30px"
            />
             &nbsp;  &nbsp; Fan Status: &nbsp; {{ this.temp>=this.threshold ? 'ON' : 'OFF' }}
          </p>
          </q-timeline-entry>
    </q-timeline>
    <img :src="temp_graph">
    <img :src="gas_graph">
  </q-page>
</template>

<script>  
export default {
  methods: {
    async getData() {
      const url = "https://ioemp.pythonanywhere.com/get";
      // const url = "http://127.0.0.1:5000/get";
      const res = await this.$axios.get(url);
      this.gas = res.data['gas'];
      this.threshold = res.data['threshold'];
      this.temp_graph = res.data['temp_graph'];      
      this.gas_graph = res.data['gas_graph'];      
      this.temp = res.data['temp'];
      console.log(this.gas,this.temp);
    },
  },
  mounted() {
    this.getData();
    setInterval(this.getData, 1000);
  },
  computed: {
    layout() {
      return this.$q.screen.lt.sm
        ? "dense"
        : this.$q.screen.lt.md
        ? "comfortable"
        : "loose";
    },
  },
  data() {
    return {
      gas: 1,
      temp:0,
      threshold:0,
      temp_graph:"data:image/png;base64,",
      gas_graph:"data:image/png;base64,"
    };
  },
};
</script>