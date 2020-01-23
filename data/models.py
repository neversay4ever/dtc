from django.db import models
import uuid

# Create your models here.

REF_VERSION_CHOICES = (
    ('hg19', 'hg19'),
    ('hg38', 'hg38'),
)

AGE_CHOICES = (
    ('child', '儿童'),
    ('adult', '成年人'),
    ('old', '老年人'),
    ('all', '不限'),
)

GENDER_CHOICES = (
    ('male', '男'),
    ('female', '女'),
    ('all', '不限'),
)

TRAIT_CATEGORY = (
    ('运动基因', '运动基因'),
    ('美容基因', '美容基因'),
    ('营养基因', '营养基因'),
    ('身体特征', '身体特征'),
    ('潜能与性格', '潜能与性格'),
)

DISEASE_CATEGORY = (
    ('遗传病', '遗传病'),
    ('肿瘤', '肿瘤'),
    ('心脑血管疾病', '心脑血管疾病'),
    ('呼吸系统疾病', '呼吸系统疾病'),
    ('消化系统疾病', '血液系统疾病'),
    ('代谢类疾病', '代谢类疾病'),
    ('免疫类疾病', '免疫类疾病'),
    ('泌尿系统疾病', '泌尿系统疾病'),
    ('生殖系统疾病', '生殖系统疾病'),
    ('皮肤系统疾病', '皮肤系统疾病'),
    ('精神心理疾病', '精神心理疾病'),
    ('眼耳疾病', '眼耳疾病'),
    ('骨骼肌肉疾病', '骨骼肌肉疾病'),
)


class Gene(models.Model):
    name = models.CharField('基因名称', max_length=20, unique=True)
    alias_name = models.CharField('别名', max_length=500, null=True, blank=True)
    chain = models.CharField('正负链', max_length=1,  default="+")
    chromosome = models.CharField('染色体', max_length=20, null=True, blank=True)
    start = models.PositiveIntegerField('起点位置', null=True, blank=True)
    end = models.PositiveIntegerField('终点位置', null=True, blank=True)
    description = models.TextField('基因介绍（英文）', null=True, blank=True)
    translation = models.TextField('基因介绍（中文）', null=True, blank=True)
    ref_version = models.CharField('参考基因组版本',
                                   max_length=20, choices=REF_VERSION_CHOICES, default="hg19")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'GENE基因'
        verbose_name_plural = 'GENE基因'

# only store snp with rs_id and simple genotype


class Snp(models.Model):
    rs_id = models.CharField('dbsnp ID', max_length=20)
    genotype = models.CharField('基因型', max_length=2)
    snp_name = models.CharField(
        '合并名称', unique=True, max_length=50, default=uuid.uuid1)
    chromosome = models.CharField('染色体', max_length=50, null=True, blank=True)
    position = models.IntegerField('位置', null=True, blank=True)
    ref_or_not = models.BooleanField(
        '是否参考基因型', null=True, blank=True, default=True)
    han_population_freq = models.FloatField('汉族人中的频率', null=True, blank=True)
    world_population_freq = models.FloatField('人群中的频率', null=True, blank=True)
    gene = models.ForeignKey('Gene', to_field='name', verbose_name='归属基因名',
                             on_delete=models.CASCADE, null=True, blank=True)
    dbsnp_version = models.PositiveSmallIntegerField(
        'dbsnp 版本号', null=True, blank=True, default=138)

    def __str__(self):
        return str(self.snp_name)

    class Meta:
        verbose_name = 'SNP突变'
        verbose_name_plural = 'SNP突变'


class Trait(models.Model):
    name = models.CharField('中文名称', max_length=50, unique=True)
    name_en = models.CharField('英文名称', max_length=50, null=True, blank=True)
    category = models.CharField('分类', max_length=50, choices=TRAIT_CATEGORY)
    introduction = models.TextField(verbose_name='背景介绍')
    advice_good = models.TextField(
        verbose_name="良好水平建议", null=True, blank=True)
    advice_avg = models.TextField(verbose_name="平均水平建议", null=True, blank=True)
    advice_bad = models.TextField(verbose_name="较弱水平建议", null=True, blank=True)
    age_choice = models.CharField(
        "年龄相关性", max_length=50, choices=AGE_CHOICES, default='all')
    gender_choice = models.CharField(
        "性别相关性", max_length=50, choices=GENDER_CHOICES, default='all')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '性状'
        verbose_name_plural = '性状'


class Disease(models.Model):
    name = models.CharField("中文名称", max_length=50, unique=True)
    name_en = models.CharField("英文名称", max_length=50, null=True, blank=True)
    category = models.CharField('分类', max_length=50, choices=DISEASE_CATEGORY)
    introduction = models.TextField(verbose_name='疾病简介')
    symptom = models.TextField(verbose_name='临床症状', null=True, blank=True)
    incidence = models.FloatField("发病率，每10万人", null=True, blank=True)
    mortality = models.FloatField("死亡率，每10万人", null=True, blank=True)
    location = models.CharField("地域", max_length=50, null=True, blank=True)
    population = models.CharField("高发人群", max_length=50, null=True, blank=True)
    age = models.CharField("好发年龄", max_length=50, null=True, blank=True)
    age_choice = models.CharField(
        "年龄分类", max_length=50, choices=AGE_CHOICES, default='all')
    gender_choice = models.CharField(
        "性别分类", max_length=50, choices=GENDER_CHOICES, default='all')
    advice_enviroment = models.TextField(
        verbose_name='环境建议', null=True, blank=True)
    advice_food = models.TextField(verbose_name='饮食建议', null=True, blank=True)
    advice_sport = models.TextField(verbose_name='运动建议', null=True, blank=True)
    advice_mental = models.TextField(
        verbose_name='心理建议', null=True, blank=True)
    advice_medical = models.TextField(
        verbose_name='医学建议', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '疾病'
        verbose_name_plural = '疾病'


class TraitSnp(models.Model):
    trait = models.ForeignKey(
        'Trait', to_field='name', on_delete=models.CASCADE, verbose_name='性状-外键')
    snp = models.ForeignKey(
        'Snp', to_field='snp_name', on_delete=models.CASCADE, verbose_name='突变-外键')
    contribution = models.FloatField(
        verbose_name='突变贡献度', null=True, blank=True)
    paper = models.ManyToManyField(
        'Paper', verbose_name='文献')

    class Meta:
        verbose_name = '性状-突变-关联'
        verbose_name_plural = '性状-突变-关联'


class DiseaseSnp(models.Model):
    disease = models.ForeignKey(
        'Disease', to_field='name', on_delete=models.CASCADE, verbose_name='疾病-外键')
    snp = models.ForeignKey(
        'Snp', to_field='snp_name', on_delete=models.CASCADE, verbose_name='突变-外键')
    or_value = models.FloatField(verbose_name='突变OR值', null=True, blank=True)
    paper = models.ManyToManyField(
        'Paper', verbose_name='文献')

    class Meta:
        verbose_name = '疾病-突变-关联'
        verbose_name_plural = '疾病-突变-关联'


class Paper(models.Model):
    title = models.CharField('标题', max_length=200, unique=True)
    journal = models.CharField('杂志', max_length=500)
    year = models.PositiveSmallIntegerField('发表时间（年）')
    abstract = models.TextField('摘要')
    citation = models.CharField('引用', max_length=250)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'PAPER文献'
        verbose_name_plural = 'PAPER文献'

# 药物类信息不全，暂不录入
# class Drug(models.Model):
#     name = models.CharField("中文名称", max_length=50, unique=True)
#     name_en = models.CharField("英文名称", max_length=50, null=True, blank=True)
#     category = models.CharField('分类', max_length=50, null=True, blank=True)
#     introduction = models.TextField(verbose_name='药物介绍', null=True, blank=True)
#     for_disease = models.TextField(verbose_name='适用疾病', null=True, blank=True)
#     drug_commodity = models.TextField(
#         verbose_name='常见药物', null=True, blank=True)
#     adverse_reaction = models.TextField(
#         verbose_name='不良反应', null=True, blank=True)
#     age_choice = models.CharField(
#         "年龄分类", max_length=50, choices=AGE_CHOICES, default='all')
#     gender_choice = models.CharField(
#         "性别分类", max_length=50, choices=GENDER_CHOICES, default='all')

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = '药物'
#         verbose_name_plural = '药物'


# class DrugSnp(models.Model):
#     drug = models.ForeignKey(
#         'Drug', to_field='name',  on_delete=models.CASCADE, verbose_name='用药-外键')
#     snp = models.ForeignKey(
#         'Snp', to_field='snp_name', on_delete=models.CASCADE, verbose_name='突变-外键')
#     dose = models.CharField('剂量', max_length=100)
#     paper = models.ManyToManyField('Paper', verbose_name='文献')

#     class Meta:
#         verbose_name = '用药-突变-关联'
#         verbose_name_plural = '用药-突变-关联'
