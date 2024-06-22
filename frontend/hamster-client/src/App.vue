<script setup>
import { ref, onMounted, watch } from 'vue';
import { useWebSocket } from '@vueuse/core'
import axios from 'axios';

const { status, data, send, open, close } = useWebSocket('ws://127.0.0.1:8000/ws')
const morse = ref('')
const users = ref([])

const morseRun = async () => {
  // const {data} = await axios.post('http://127.0.0.1:8000/morse', {
  //   code: morse.value
  // })
  console.log(data)
}

const getUsers = async () => {
  try{
    const {data} = await axios.get('http://127.0.0.1:8000/users')
    users.value = data
  } catch (e) {
    console.log(e)
  }
}

const messages = ref([])

onMounted(() => {
  getUsers()
  watch(data, (newValue) => {
    messages.value = JSON.parse(newValue)
  })
})

</script>

<template>
  
  <div class="wrapper">
    <div class="main-console">
      <div class="main-console-content" v-if="messages.length === 0">
        <span class="console-text">Нет активных логов</span>
      </div>
      <div class="main-console-content" v-for="item in messages" v-else>
        <span class="main-console-user">hmstBot</span>
        <div class="console-text">=========Информация================================</div>
        <div>
          Пользователь: {{ item.userID }}
        </div>
        <div>
          Логи: {{ item.msg }}
        </div>

        <div class="console-text">===================================================</div>
      </div>
    </div>
    
    <div class="main-button-task">
      <div class="morse">
        <div class="users-text">
          <span>Пользователи</span>
        </div>
        <div v-for="item in users" class="test">
          <div class="main-users">
            <div class="circle">

            </div>
            <div>
              {{ item.token }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div>
      <iframe width="600" height="300" src="https://www.youtube.com/embed/qsyWZrwsN4k?si=sDZJpdLJmeY2jEIb" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


      <div class="text-information">
      </div>

    </div>


  </div>

  <!-- <div v-for="(item, index) in messages" :key="index">
    {{ item.userID }} || {{ item.count }}
  </div> -->
</template>

<style scoped>
.morse {
  text-align: center;
  border: 1px solid white;
  height: 398px;
  border-radius: 10px;
  overflow-x: auto;
}

.text-information {
  margin-top: 10px;
}

.information-block-main {
  border: 1px solid white;
  border-radius: 10px;
  text-align: center;
}


.circle {
  width: 2em;
  margin-left: 5px;
  margin-right: 5px;
  margin-bottom: 10px;
  border-radius: 50%;
  background-color: rgb(4, 253, 25);
}

.circle::before{
  content: "";
  display: inline-block;
  vertical-align: middle;
  padding-top: 100%;
}

.main-users {
  display: flex;
  align-items: center;
  justify-content: center;
}

.users-text {
  margin-bottom: 5px;
}

.morse-btn {
  margin-top: 10px;
}

.morse-input {
  margin-top: 10px;
}


.wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  margin-top: 10px;
  padding: 10px;
}

.main-console {
  display: block;
  background-color: black;
  height: 400px;
  box-shadow: 10px 5px 5px rgb(10, 10, 10);
  overflow-x: auto;
  border-radius: 10px;
}

.main-button-task {
  margin-left: 10px;
  margin-right: 10px;
}

.main-console-content {
  padding: 10px;
}

.main-console-user {
  color: #f7d07e;
}

.console-text {
  color: rgb(8, 240, 8);
}

</style>