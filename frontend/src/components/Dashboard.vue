<template>
  <div>
    <h2>Dashboard</h2>
    <p>Books</p>
    <ul>
      <li v-for=\"b in books\" :key=\"b\"><router-link :to=\"`/books/${b}`\">{{b}}</router-link></li>
    </ul>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  data(){ return { books: [] } },
  async created(){
    try{
      const res = await axios.get('/books')
      this.books = res.data.map(b=>b.name)
    }catch(e){ console.log(e) }
  }
}
</script>

</script>
>>>>>>> 1c071df926c702b72a64ef539685c19e319a01de
