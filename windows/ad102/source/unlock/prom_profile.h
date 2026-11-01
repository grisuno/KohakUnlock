#ifndef GU_PROM_PROFILE_H
#define GU_PROM_PROFILE_H
/* Local AD102 NVGI dump: two identical expansion views at +0x9400 and
 * +0xe9400. Live PROM mapping is verified against this hash BEFORE writes;
 * its correspondence to BAR0+0x300000 is not assumed to be hardware-tested. */
#define GU_PROM_BAR_OFFSET 0x300000U
#define GU_PROM_VIEW_BYTES 0xd6c00U
#define GU_PROM_VIEW_SHA256 "18a54e8d9e0ec61778cf275f6d3438c6d1d46d94fa558bb6541b65476305f22a"
#endif
