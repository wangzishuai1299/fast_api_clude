<template>
    <el-card style="max-width: 80%">
        <template #header>
            <div class="card-header">
                <el-input v-model="search_meassage" style="width: 240px" placeholder="请输入搜索内容" /> <el-button
                    @click="sousuo">搜索</el-button>
                <br>
                <el-button type="primary" plain @click="view">新增客房</el-button>
            </div>
        </template>
        <p>
            <el-table :data="tableData" style="width: 100%">
                <el-table-column prop="id" label="ID" width="100" />
                <el-table-column prop="name" label="房号" width="160" />
                <el-table-column prop="room_type" label="房间类型" width="160" />
                <el-table-column prop="floor" label="楼层" />
                <el-table-column prop="bedCount" label="床位数量" />
                <el-table-column prop="price" label="价格" />
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="primary" @click="handleEdit(scope.row)">编辑</el-button>
                        <el-button type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
                    </template>
                </el-table-column>

            </el-table>
        </p>
        <template #footer>
              <el-pagination
    :page-size="20"
    :pager-count="11"
    layout="prev, pager, next"
    :total="100"
  />
        </template>
    </el-card>


    <el-dialog v-model="dialogFormVisible" :title="edit_id?'修改客房信息':'新增客房信息'" width="500">
        <el-form :model="form">
            <el-form-item label="房号" :label-width="formLabelWidth">
                <el-input v-model="form.name" autocomplete="off" />
            </el-form-item>

            <el-form-item label="房间类型" :label-width="formLabelWidth">
                <el-input v-model="form.room_type" autocomplete="off" />
            </el-form-item>

            <el-form-item label="楼层" :label-width="formLabelWidth">
                <el-input v-model="form.floor" autocomplete="off" />
            </el-form-item>

            <el-form-item label="床位数量" :label-width="formLabelWidth">
                <el-input v-model="form.bedCount" autocomplete="off" />
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
import { ref, reactive, onMounted } from 'vue'
import service from './router/index.js'
import { ElMessage, ElMessageBox } from 'element-plus'
const tableData = ref([])
const page = ref(1)
const search_meassage = ref('')

const dialogFormVisible = ref(false)
const formLabelWidth = '140px'
const form = reactive({
    name: '',
    room_type: '',
    floor: '',
    bedCount: '',
    price: ''
})

onMounted(() => {
    loadData()
})


const loadData = async () => {
    const params = {
        page: page.value,
        pageSize: 10
    }
    if (search_meassage.value) {
        params['keywords'] = search_meassage.value
    }
    const res = await service.get('/rooms', { params })
    console.log(res.data.items)
    tableData.value = res.data.items
}
const sousuo = () => {
    loadData()
}

const edit_id = ref('')
const view = () => {
    if (edit_id.value) {
        form.name = '',
            form.room_type = '',
            form.floor = '',
            form.bedCount = '',
            form.price = ''
    }
    dialogFormVisible.value = true
}

const handleClick = async () => {
    if(edit_id.value){
        await service.put(`/rooms/${edit_id.value}`, form)

    }else{
        await service.post('/rooms', form)
         form.name = ''
        form.room_type = ''
        form.floor = ''
        form.bedCount = ''
        form.price = ''
    }
    
    dialogFormVisible.value = false
    loadData()
}

const handleDelete = async (id) => {
    ElMessageBox.confirm(
        '是否确定删除当前所有房间信息？',
        '警告',
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )
        .then(async () => {
            await service.delete(`/rooms/${id}`)
            loadData()
            ElMessage({
                type: 'success',
                message: '删除成功',
            })
        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: '取消成功',
            })
        })
}

const handleEdit = async (row) => {
    edit_id.value = row.id
    Object.assign(form, {
        name: row.name,
        room_type: row.room_type,
        floor: row.floor,
        bedCount: row.bedCount,
        price: row.price
    })
    dialogFormVisible.value = true
}





</script>

<style scoped>
:deep(.el-table .el-table__cell){
    text-align: center;

}

</style>