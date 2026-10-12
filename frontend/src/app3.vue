<template>
    <table border width="400px">
        <tr>
            <th>id</th>
            <th>分类名称</th>
            <th>分类描述</th>
        </tr>
        <tr>
            <td>1</td>
            <td>数码类</td>
            <td>手机，电脑</td>
        </tr>
        <tr>
            <td>2</td>
            <td>衣服类</td>
            <td>毛衣，秋裤</td>
        </tr>
    </table>

    <el-card style="max-width: 70%">
        <template #header>
            <div class="card-header">
                  <el-input v-model="search_message" style="width: 240px" placeholder="Please input" /> <el-button @click="loadData()">搜索</el-button>
            </div>

            <hr>
             <el-button  @click="view">
      增加
    </el-button>
        </template>
        <p>
            <el-table :data="tableData" style="width: 80%">
                <el-table-column prop="id" label="ID" width="180" />
                <el-table-column prop="category_name" label="分类" width="180" />
                <el-table-column prop="goods_name" label="商品" />
                <el-table-column prop="price" label="价格" />
            </el-table>
        </p>
        <template #footer>Footer content</template>
    </el-card>

      <el-dialog v-model="dialogFormVisible" title="Shipping address" width="500">
    <el-form :model="form">
      <el-form-item label="商品分类" :label-width="formLabelWidth">
        <el-input v-model="form.goods_id" autocomplete="off" />
      </el-form-item>

       <el-form-item label="名称" :label-width="formLabelWidth">
        <el-input v-model="form.goods_name" autocomplete="off" />
      </el-form-item>

        <el-form-item label="价格" :label-width="formLabelWidth">
        <el-input v-model="form.price" autocomplete="off" />
      </el-form-item>

    


     
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogFormVisible = false">Cancel</el-button>
        <el-button type="primary" @click="handleClick">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>

</template>

<script setup>
import { ref, reactive,onMounted } from 'vue'
import  service from './router/index.js'

const search_message = ref('')
const page = ref(1)

const dialogFormVisible = ref(false)
const formLabelWidth = '140px'
const form = reactive({
    goods_id: '',
    goods_name: '',
    price: ''
})
onMounted(()=>{
    loadData()
})

const loadData=async()=>{
    const params={
        page:page.value,
        pageSize:10
    }
    if (search_message.value){
        params['keywords']=search_message.value
    }
    const res = await service.get('/goods',{params})
    tableData.value=res.data.items


}

const tableData = ref([])

const view=()=>{
    dialogFormVisible.value=true

}
const handleClick=async()=>{
    await service.post('/goods',form)
    dialogFormVisible.value=false
    loadData()

    
}


</script>
