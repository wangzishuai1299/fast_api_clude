<template>
    <el-card style="max-width: 80%">
        <template #header>
             <el-input v-model="search_message" style="width: 240px" placeholder="Please input" @keydown.enter="sousuo" /> 
             <el-button @click="sousuo">搜索</el-button>
             <br>
             <el-button  @click="view">
      新增信息
    </el-button>

        </template>
        <p>
            <el-table :data="tableData" style="width: 100%">
                <el-table-column prop="id" label="ID" width="180" />
                <el-table-column prop="name" label="商品名称" width="180" />
                <el-table-column prop="brand" label="品牌" />
                <el-table-column prop="price" label="价格" />
                <el-table-column prop="stock" label="库存" />

                     <el-table-column>
                        <template #default="scope">
                    <el-button type="primary" @click="handleEdit(scope.row)">编辑</el-button>
                    <el-button type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
                      </template>
                </el-table-column>


            </el-table>

        </p>
        <template #footer>Footer content</template>
    </el-card>

      <el-dialog v-model="dialogFormVisible" title="Shipping address" width="500">
    <el-form :model="form">
      <el-form-item label="商品名称" :label-width="formLabelWidth">
        <el-input v-model="form.name" autocomplete="off" />
      </el-form-item>

      <el-form-item label="品牌" :label-width="formLabelWidth">
        <el-input v-model="form.brand" autocomplete="off" />
      </el-form-item>

      <el-form-item label="价格" :label-width="formLabelWidth">
        <el-input v-model="form.price" autocomplete="off" />
      </el-form-item>

      <el-form-item label="库存" :label-width="formLabelWidth">
        <el-input v-model="form.stock" autocomplete="off" />
      </el-form-item>
     
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAdd">
          确认
        </el-button>
      </div>
    </template>
  </el-dialog>

</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
const tableData = ref([])
const search_message=ref('')
const page=ref(1)
import { ElMessage, ElMessageBox } from 'element-plus'


const dialogFormVisible = ref(false)
const formLabelWidth = '140px'
const form = reactive({
    name:"",
    brand:"",
    price:"",
    stock:"",
})

import service from './router/index.js'

onMounted(() => {
    loadData()
})

const loadData = async () => {
    const params = {
        page: page.value,
        page_size: 10
    }
    if (search_message.value) {
        params['keywords'] = search_message.value
    }

    const res = await service.get('/goods',{params})
    tableData.value = res.data.goods
}
const sousuo=()=>{
    loadData()
}
const edit_id=ref('')

const view=()=>{
    if (edit_id.value){
        form.name=''
        form.brand=''
        form.price=''
        form.stock=''
        
    }
    dialogFormVisible.value = true

}

const handleAdd = async () => {

    if (edit_id.value){
        await service.put(`/goods/${edit_id.value}`, form)
        
    }
    else {
       await service.post('/goods', form)
    
    }
    dialogFormVisible.value = false
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
        await service.delete(`/goods/${id}`)
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
    edit_id.value=row.id
    Object.assign(form,{
        name:row.name,
        brand:row.brand,
        price:row.price,
        stock:row.stock
    })
    dialogFormVisible.value = true
}








</script>

<style></style>