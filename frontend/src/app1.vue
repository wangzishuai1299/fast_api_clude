<template>
  <el-card style="max-width: 80%">
    <template #header>
      <div class="card-header">
        <el-input v-model="search_message" style="width: 240px" placeholder="Please input" /> <el-button @click="sousuo">搜索</el-button>
      </div>
      <hr>
          <el-button  @click="view">
      新增信息
    </el-button>
    </template>
    <p>
         <el-table :data="tableData" style="width: 100%">
    <el-table-column prop="id" label="ID" width="180" />
    <el-table-column prop="name" label="名称" width="180" />
    <el-table-column prop="production_factory" label="厂商" />
    <el-table-column prop="stock" label="库存" />
    <el-table-column prop="price" label="价格" />
     <el-table-column label="操作">
        <template #default="scope">
            <el-button @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
        </template>
        
     </el-table-column>
  </el-table>


    </p>
    <template #footer>

    </template>
  </el-card>

 <el-dialog v-model="dialogFormVisible" title="Shipping address" width="500">
    <el-form :model="form">
      <el-form-item label="药品名称" :label-width="formLabelWidth">
        <el-input v-model="form.name" autocomplete="off" />
      </el-form-item>

      <el-form-item label="制药厂商" :label-width="formLabelWidth">
        <el-input v-model="form.production_factory" autocomplete="off" />
      </el-form-item>

      <el-form-item label="库存" :label-width="formLabelWidth">
        <el-input v-model="form.stock" autocomplete="off" />
      </el-form-item>

      <el-form-item label="价格" :label-width="formLabelWidth">
        <el-input v-model="form.price" autocomplete="off" />
      </el-form-item>

    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="handleClick">
          确认
        </el-button>
      </div>
    </template>
  </el-dialog>

</template>

<script setup>
import {ref,reactive,onMounted} from 'vue'
import service from './router/index.js'
import { ElMessage, ElMessageBox } from 'element-plus'

const tableData = ref([])
const page=ref(1)
const search_message=ref('')
const dialogFormVisible = ref(false)
const formLabelWidth = '140px'

const form = reactive({
    name:"",
    production_factory:"",
    stock:"",
    price:""

})

onMounted(()=>{
    loadData()
})

const loadData =async ()=>{
    const params={
        page:page.value,
        pageSize:10
    }
    if (search_message.value){
        params['keywords']=search_message.value
    }
    const res = await service.get('/medicine',{params})
    tableData.value=res.data.items

}

const sousuo=()=>{
    loadData()
}
const editId=ref('')
const view=()=>{
    if (editId.value){
        form.name='',
        form.production_factory="",
        form.stock="",
        form.price=""
    }
     dialogFormVisible.value=true
}

const handleClick= async()=>{
    
    if (editId.value){
        await service.put(`/medicine/${editId.value}`,form)
    }else{

    await service.post('/medicine',form)
    
}
dialogFormVisible.value=false
    loadData()
}


const handleDelete=async(id)=>{
      ElMessageBox.confirm(
    'proxy will permanently delete the file. Continue?',
    'Warning',
    {
      confirmButtonText: 'OK',
      cancelButtonText: 'Cancel',
      type: 'warning',
    }
  )
    .then(async() => {
      await service.delete(`/medicine/${id}`)
      loadData()
      ElMessage({
        type: 'success',
        message: 'Delete completed',
      })
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: 'Delete canceled',
      })
    })
}

const handleEdit=async(row)=>{
    editId.value=row.id
    Object.assign(form,{
        name:row.name,
        production_factory:row.production_factory,
        stock:row.stock,
        price:row.price
    })
    dialogFormVisible.value=true
}

</script>

<style>

</style>