<template>
  <div>
    <h3>Book: {{bookName}}</h3>
    <button @click=\"addRow\">Add Row</button>
    <button @click=\"saveAll\">Save All</button>
    <button @click=\"exportSummary\">Export Daily Summary</button>
    <table border=\"1\" cellpadding=\"4\">
      <thead><tr><th>Date</th><th>Item</th><th>Qty</th><th>Rate</th><th>Total</th><th>Patient</th><th>Department</th></tr></thead>
      <tbody>
        <tr v-for=\"(r,i) in rows\" :key=\"i\">
          <td><input v-model=\"r.date\" type=\"date\" /></td>
          <td><input v-model=\"r.item\" /></td>
          <td><input v-model.number=\"r.quantity\" /></td>
          <td><input v-model.number=\"r.rate\" /></td>
          <td>{{ (r.quantity||0) * (r.rate||0) }}</td>
          <td><input v-model=\"r.patient\" /></td>
          <td><input v-model=\"r.department\" /></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  data(){ return { rows: [], bookName: this.$route.params.name } },
  methods:{
    addRow(){ this.rows.push({ date: new Date().toISOString().slice(0,10), item:'', quantity:1, rate:0, patient:'', department:'' }) },
    async saveAll(){
      for(const r of this.rows){
        await axios.post('/transactions', {...r, book_name: this.bookName}, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
      }
      alert('Saved')
      this.rows = []
    },
    async exportSummary(){
      const res = await axios.get(`/books/${this.bookName}/daily-summary/export`, { responseType: 'blob', headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
      const url = window.URL.createObjectURL(new Blob([res.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `${this.bookName}_daily_summary.xlsx`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    }
  }
}
</script>
