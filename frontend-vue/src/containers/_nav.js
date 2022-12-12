export default [
  {
    _name: 'CSidebarNav',
    _children: [
      {
        _name: 'CSidebarNavItem',
        name: '진동센서 실시간 대시보드',
        to: '/manager/dashboard',
        icon: 'cil-speedometer',
      },
      {
        _name: 'CSidebarNavItem',
        name: '전력센서 실시간 대시보드',
        to: '/manager/dashboard_power',
        icon: 'cil-speedometer',
      },      
      // {
      //   _name: 'CSidebarNavItem',
      //   name: '사출기 데이터',
      //   to: '/manager/injectiondata',
      //   icon: 'cil-layers',
      // },
      {
        _name: 'CSidebarNavItem',
        name: '공작기계 진동 데이터',
        to: '/manager/cncoscidata',
        icon: { name: 'cilAudioSpectrum', class: 'text-white' },
      },
      {
        _name: 'CSidebarNavItem',
        name: '공작기계 전력 데이터',
        to: '/manager/cncpower',
        icon: { name: 'cilBolt', class: 'text-white' },
      },
      {
        _name: 'CSidebarNavItem',
        name: '주피터허브',
        href: 'http://192.168.137.2:39470',
        target:"_blank",
        icon: { name: 'cilSchool', class: 'text-white' },
      },
      {
        _name: 'CSidebarNavItem',
        name: '사용자 관리',
        to: '/manager/users',
        icon: { name: 'cil-group', class: 'text-white' },
      },        
    ]
  }
]