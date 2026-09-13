(function () {
    if (document.documentElement.lang !== 'ar') return;

    const translations = {
        'Home': 'الرئيسية', 'Leads': 'العملاء المحتملون', 'Properties': 'العقارات',
        'Opportunities': 'الفرص', 'Tasks': 'المهام', 'Documents': 'المستندات',
        'Analytics': 'التحليلات', 'Admin': 'الإدارة', 'CRM': 'إدارة علاقات العملاء',
        'Lead Sources': 'مصادر العملاء المحتملين', 'Lead Statuses': 'حالات العملاء المحتملين',
        'Real Estate': 'العقارات', 'Property Types': 'أنواع العقارات',
        'Property Statuses': 'حالات العقارات', 'Sales': 'المبيعات',
        'Pipeline Stages': 'مراحل المبيعات', 'Task Management': 'إدارة المهام',
        'My Tasks': 'مهامي', 'Categories': 'التصنيفات', 'Priorities': 'الأولويات',
        'Statuses': 'الحالات', 'Administration': 'الإدارة', 'Notifications': 'الإشعارات',
        'Reports': 'التقارير', 'Admin Panel': 'لوحة الإدارة', 'Dashboard': 'لوحة التحكم',
        'Manage your sales leads': 'إدارة العملاء المحتملين للمبيعات',
        'Manage your properties': 'إدارة العقارات', 'Manage your tasks': 'إدارة المهام',
        'Manage lead status workflow': 'إدارة سير عمل حالات العملاء المحتملين',
        'Manage lead sources': 'إدارة مصادر العملاء المحتملين',
        'Add Lead': 'إضافة عميل محتمل', 'Add Property': 'إضافة عقار', 'Add Task': 'إضافة مهمة',
        'Add Source': 'إضافة مصدر', 'Add Status': 'إضافة حالة', 'Add Opportunity': 'إضافة فرصة',
        'Add Document': 'إضافة مستند', 'Edit': 'تعديل', 'Delete': 'حذف', 'View': 'عرض',
        'View Details': 'عرض التفاصيل', 'Back': 'رجوع', 'Back to List': 'العودة إلى القائمة',
        'Cancel': 'إلغاء', 'Save': 'حفظ', 'Create': 'إنشاء', 'Update': 'تحديث',
        'Close': 'إغلاق', 'Search': 'بحث', 'Clear': 'مسح', 'Apply': 'تطبيق',
        'Actions': 'الإجراءات', 'Name': 'الاسم', 'First Name': 'الاسم الأول',
        'Last Name': 'اسم العائلة', 'Full Name': 'الاسم الكامل', 'Email': 'البريد الإلكتروني',
        'Phone': 'الهاتف', 'Company': 'الشركة', 'Address': 'العنوان', 'City': 'المدينة',
        'State': 'المحافظة', 'Country': 'الدولة', 'Description': 'الوصف', 'Notes': 'الملاحظات',
        'Status': 'الحالة', 'Priority': 'الأولوية', 'Source': 'المصدر', 'Assigned To': 'مسند إلى',
        'Created': 'تاريخ الإنشاء', 'Created At': 'تاريخ الإنشاء', 'Due Date': 'تاريخ الاستحقاق',
        'All Status': 'كل الحالات', 'All Statuses': 'كل الحالات', 'All Priority': 'كل الأولويات',
        'All Sources': 'كل المصادر', 'No leads found.': 'لم يتم العثور على عملاء محتملين.',
        'No properties found.': 'لم يتم العثور على عقارات.', 'No tasks found.': 'لم يتم العثور على مهام.',
        'No results found.': 'لم يتم العثور على نتائج.', 'Contact Information': 'معلومات الاتصال',
        'Lead Details': 'تفاصيل العميل المحتمل', 'Additional Info': 'معلومات إضافية',
        'Property Details': 'تفاصيل العقار', 'Import / Export': 'استيراد / تصدير',
        'Export as CSV': 'تصدير بصيغة CSV', 'Export as Excel': 'تصدير بصيغة Excel',
        'Import from File': 'استيراد من ملف', 'Import Leads': 'استيراد العملاء المحتملين',
        'Import Properties': 'استيراد العقارات', 'Upload File': 'رفع ملف',
        'Upload & Map Columns': 'رفع ومطابقة الأعمدة', 'Map Columns': 'مطابقة الأعمدة',
        'Preview': 'معاينة', 'Data preview': 'معاينة البيانات', 'Import Summary': 'ملخص الاستيراد',
        'Total Rows': 'إجمالي الصفوف', 'Rows per page:': 'الصفوف لكل صفحة:',
        'Showing': 'عرض', 'of': 'من', 'Save view': 'حفظ العرض', 'Save current filter': 'حفظ الفلتر الحالي',
        'Filter and columns': 'الفلاتر والأعمدة', 'Load saved filter': 'تحميل فلتر محفوظ',
        'Choose columns to show': 'اختر الأعمدة المعروضة', 'Name this filter': 'اسم الفلتر',
        'Name this view': 'اسم العرض', 'Reset': 'إعادة ضبط', 'Apply filters': 'تطبيق الفلاتر',
        'All fields are optional.': 'جميع الحقول اختيارية.', 'Import complete': 'اكتمل الاستيراد',
        'Calls': 'المكالمات', 'Meetings': 'الاجتماعات', 'Emails': 'رسائل البريد', 'Tasks': 'المهام',
        'Notes': 'الملاحظات', 'Activity': 'النشاط', 'Timeline': 'المخطط الزمني',
        'Are you sure you want to delete this item?': 'هل أنت متأكد من حذف هذا العنصر؟',
        'Yes, delete': 'نعم، احذف', 'No, go back': 'لا، عودة', 'Login': 'تسجيل الدخول',
        'Sign In': 'تسجيل الدخول', 'Sign Out': 'تسجيل الخروج', 'Username': 'اسم المستخدم',
        'Password': 'كلمة المرور', 'Register': 'تسجيل', 'Profile': 'الملف الشخصي',
        'Welcome': 'مرحباً', 'Language': 'اللغة', 'Change language': 'تغيير اللغة'
        , 'Analytics & Reports': 'التحليلات والتقارير',
        'Comprehensive business intelligence overview': 'نظرة شاملة على ذكاء الأعمال',
        'Detailed Reports': 'التقارير التفصيلية', 'Leads Report': 'تقرير العملاء المحتملين',
        'Properties Report': 'تقرير العقارات', 'Opportunities Report': 'تقرير الفرص',
        'Tasks Report': 'تقرير المهام', 'Agent Performance': 'أداء الموظفين',
        'Pipeline Report': 'تقرير مسار المبيعات', 'Revenue Report': 'تقرير الإيرادات',
        'Sources, status, priority, agent performance': 'المصادر والحالة والأولوية وأداء الموظفين',
        'Types, prices, cities, features': 'الأنواع والأسعار والمدن والمميزات',
        'Pipeline, win rate, types, monthly trends': 'المسار ومعدل الفوز والأنواع والاتجاهات الشهرية',
        'Completion, overdue, agent load': 'الإنجاز والمتأخر وأعباء الموظفين',
        'Per-agent leads, deals, tasks': 'العملاء والصفقات والمهام لكل موظف',
        'Monthly revenue, closed deals, avg deal size': 'الإيرادات الشهرية والصفقات المغلقة ومتوسط قيمة الصفقة',
        'Stage analysis, conversion funnel': 'تحليل المراحل ومسار التحويل',
        'Total Leads': 'إجمالي العملاء المحتملين', 'Active Properties': 'العقارات النشطة',
        'Pipeline Value': 'قيمة مسار المبيعات', 'Win Rate': 'معدل الفوز',
        'Closed Won': 'الصفقات الرابحة المغلقة', 'Task Completion': 'إنجاز المهام',
        'Total Properties': 'إجمالي العقارات', 'Total Value': 'إجمالي القيمة',
        'Average Price': 'متوسط السعر', 'Total Deals': 'إجمالي الصفقات',
        'Won Deals': 'الصفقات الرابحة', 'Revenue Won': 'الإيرادات المحققة',
        'Total Tasks': 'إجمالي المهام', 'Completed': 'مكتملة', 'Pending': 'معلقة',
        'Overdue': 'متأخرة', 'Completion Rate': 'معدل الإنجاز', 'Active Agents': 'الموظفون النشطون',
        'Total Deals': 'إجمالي الصفقات', 'Total Revenue': 'إجمالي الإيرادات',
        'Closed Deals': 'الصفقات المغلقة', 'Avg Deal Size': 'متوسط قيمة الصفقة',
        'Leads by Status': 'العملاء المحتملون حسب الحالة', 'Leads by Source': 'العملاء المحتملون حسب المصدر',
        'Leads by Priority': 'العملاء المحتملون حسب الأولوية', 'Leads by Agent': 'العملاء المحتملون حسب الموظف',
        'Properties by Type': 'العقارات حسب النوع', 'Properties by Status': 'العقارات حسب الحالة',
        'Properties by City': 'العقارات حسب المدينة', 'Price Distribution': 'توزيع الأسعار',
        'Features Overview': 'نظرة عامة على المميزات', 'Property Data': 'بيانات العقارات',
        'Garage': 'مرآب', 'Pool': 'مسبح', 'Garden': 'حديقة', 'Pet Friendly': 'مناسب للحيوانات الأليفة',
        'Featured': 'مميز', 'Opportunities by Stage': 'الفرص حسب المرحلة',
        'Opportunities by Type': 'الفرص حسب النوع', 'Opportunities by Agent': 'الفرص حسب الموظف',
        'Monthly Trends': 'الاتجاهات الشهرية', 'Opportunity Data': 'بيانات الفرص',
        'Tasks by Status': 'المهام حسب الحالة', 'Tasks by Priority': 'المهام حسب الأولوية',
        'Tasks by Category': 'المهام حسب التصنيف', 'Tasks by Agent': 'المهام حسب الموظف',
        'Task Data': 'بيانات المهام', 'Agent Metrics': 'مؤشرات الموظفين',
        'Monthly Revenue': 'الإيرادات الشهرية', 'Revenue by Type': 'الإيرادات حسب النوع',
        'Monthly Breakdown': 'التفصيل الشهري', 'Leads': 'العملاء المحتملون',
        'Properties': 'العقارات', 'Opportunities': 'الفرص', 'Agents': 'الموظفون',
        'Pipeline': 'مسار المبيعات', 'Revenue': 'الإيرادات', 'Deals Closed': 'الصفقات المغلقة',
        'Deal Value': 'قيمة الصفقة', 'Close Date': 'تاريخ الإغلاق', 'Type': 'النوع',
        'Stage': 'المرحلة', 'Won': 'رابحة', 'Open': 'مفتوحة', 'No closed deals yet': 'لا توجد صفقات مغلقة بعد',
        'No data': 'لا توجد بيانات', 'No revenue data': 'لا توجد بيانات إيرادات',
        'No opportunities found': 'لم يتم العثور على فرص', 'No agents found': 'لم يتم العثور على موظفين',
        'Opportunities': 'الفرص', 'Properties': 'العقارات', 'Tasks': 'المهام', 'Leads': 'العملاء المحتملون',
        'Agent': 'الموظف', 'Deals': 'الصفقات', 'Completion': 'الإنجاز', 'Month': 'الشهر',
        'Revenue': 'الإيرادات', 'Avg Deal': 'متوسط الصفقة', 'Stage analysis, conversion funnel & deal flow': 'تحليل المراحل ومسار التحويل وتدفق الصفقات',
        'Total in Pipeline': 'إجمالي المسار', 'Total Pipeline Value': 'إجمالي قيمة المسار',
        'Pipeline Funnel': 'مسار المبيعات', 'Stage Details': 'تفاصيل المراحل',
        'Total Value': 'إجمالي القيمة', 'Avg Value': 'متوسط القيمة', '% of Pipeline': 'النسبة من المسار',
        'No pipeline data': 'لا توجد بيانات لمسار المبيعات',
        'Analytics & Reports - Cairobrokers CRM': 'التحليلات والتقارير - القاهرة للوساطة العقارية',
        'Leads Report - Cairobrokers CRM': 'تقرير العملاء المحتملين - القاهرة للوساطة العقارية',
        'Properties Report - Cairobrokers CRM': 'تقرير العقارات - القاهرة للوساطة العقارية',
        'Opportunities Report - Cairobrokers CRM': 'تقرير الفرص - القاهرة للوساطة العقارية',
        'Tasks Report - Cairobrokers CRM': 'تقرير المهام - القاهرة للوساطة العقارية',
        'Agent Performance - Cairobrokers CRM': 'أداء الموظفين - القاهرة للوساطة العقارية',
        'Pipeline Report - Cairobrokers CRM': 'تقرير مسار المبيعات - القاهرة للوساطة العقارية',
        'Revenue Report - Cairobrokers CRM': 'تقرير الإيرادات - القاهرة للوساطة العقارية',
        'List': 'قائمة', 'Cards': 'بطاقات', 'List View': 'عرض القائمة', 'Grid View': 'عرض البطاقات',
        'Add Property': 'إضافة عقار', 'Add Property Status': 'إضافة حالة عقار',
        'Add Property Type': 'إضافة نوع عقار', 'Edit Property': 'تعديل العقار',
        'Delete Property': 'حذف العقار', 'Yes, Delete Property': 'نعم، احذف العقار',
        'Back to Properties': 'العودة إلى العقارات', 'Export as CSV': 'تصدير بصيغة CSV',
        'Export as Excel': 'تصدير بصيغة Excel', 'Add Unit': 'إضافة وحدة',
        'Add Viewing': 'إضافة معاينة', 'Add Offer': 'إضافة عرض', 'Add Note': 'إضافة ملاحظة',
        'Save Changes': 'حفظ التغييرات', 'View': 'عرض', 'Edit': 'تعديل', 'Delete': 'حذف',
        'Yes, delete': 'نعم، احذف', 'No, go back': 'لا، عودة', 'Import / Export': 'استيراد / تصدير',
        'Import from File': 'استيراد من ملف', 'Upload & Map Columns': 'رفع ومطابقة الأعمدة',
        'Add Meeting': 'إضافة اجتماع', 'Add Task': 'إضافة مهمة', 'Add Email': 'إضافة بريد إلكتروني',
        'Log Call': 'تسجيل مكالمة', 'Log Email': 'تسجيل بريد إلكتروني', 'Complete': 'إكمال',
        'Mark Read': 'تحديد كمقروء', 'Archive': 'أرشفة', 'More Actions': 'إجراءات إضافية',
        'Save': 'حفظ', 'Cancel': 'إلغاء', 'Back to List': 'العودة إلى القائمة'
    };

    const translateValue = function (value) {
        const trimmed = value.trim();
        return translations[trimmed] || value;
    };

    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const textNodes = [];
    while (walker.nextNode()) textNodes.push(walker.currentNode);
    textNodes.forEach(function (node) {
        if (!node.parentElement.closest('script, style, textarea')) node.nodeValue = translateValue(node.nodeValue);
    });

    document.querySelectorAll('input[placeholder], textarea[placeholder], [title], [aria-label]').forEach(function (element) {
        ['placeholder', 'title', 'aria-label'].forEach(function (attribute) {
            if (element.hasAttribute(attribute)) element.setAttribute(attribute, translateValue(element.getAttribute(attribute)));
        });
    });

    if (document.title) document.title = translateValue(document.title);
    if (window.Chart && Chart.instances) {
        Chart.defaults.font.family = "'Cairo','Tahoma','Arial',sans-serif";
        Object.values(Chart.instances).forEach(function (chart) {
            const options = chart.options || {};
            if (options.plugins && options.plugins.title && options.plugins.title.text) {
                options.plugins.title.text = translateValue(options.plugins.title.text);
            }
            if (chart.data.labels) chart.data.labels = chart.data.labels.map(translateValue);
            (chart.data.datasets || []).forEach(function (dataset) {
                if (dataset.label) dataset.label = translateValue(dataset.label);
            });
            chart.update();
        });
    }
})();
