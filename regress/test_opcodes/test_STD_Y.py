#! /usr/bin/env python
###############################################################################
#
# simulavr - A simulator for the Atmel AVR family of microcontrollers.
# Copyright (C) 2001, 2002  Theodore A. Roth
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
###############################################################################
#
# $Id: test_STD_Y.py,v 1.1 2004/07/31 00:59:11 rivetwa Exp $
#

"""Test the STD_Y opcode.
"""

import base_test
from registers import Reg, SREG

class STD_Y_TestFail(base_test.TestFail): pass

class base_STD_Y(base_test.opcode_test):
	"""Generic test case for testing STD_Y opcode.

	STD_Y - Store Indirect to data space from Register using index Y with
	displacement, q.

	Operation: (Y+q) <- Rd

	opcode is '10q0 qq1d dddd 1qqq' where 0 <= d <= 31, 0 <= q <= 63

	Only registers PC should be changed.
	"""
	def setup(self):
		# Set the register values
		self.setup_regs[self.Rd] = self.Vd
		self.setup_regs[Reg.R28] = (self.Y & 0xff)
		self.setup_regs[Reg.R29] = (self.Y >> 8)

		# Return the raw opcode
		op_q = ((self.q & 0x20) << 8) | ((self.q & 0x18) << 7) | (self.q & 0x3)
		return 0x8208 | (self.Rd << 4) | op_q

	def analyze_results(self):
		# check that result is correct
		
		# FIXME: [TRoth 2002/04/04] Is this really what we should expect?
		if self.Rd == Reg.R28:
			expect = self.setup_regs[Reg.R28]
		elif self.Rd == Reg.R29:
			expect = self.setup_regs[Reg.R29]
		else:			
			expect = self.Vd

		got = self.mem_byte_read( self.Y + self.q )
		
		if expect != got:
			self.fail('STD_Y: expect=%02x, got=%02x' % (expect, got))

#
# Template code for test case.
# The fail method will raise a test specific exception.
#
template = """
class STD_Y_r%02d_Y%04x_q%02x_v%02x_TestFail(STD_Y_TestFail): pass

class test_STD_Y_r%02d_Y%04x_q%02x_v%02x(base_STD_Y):
	Rd = %d
	Y = 0x%x
	q = 0x%x
	Vd = 0x%x
	def fail(self,s):
		raise STD_Y_r%02d_Y%04x_q%02x_v%02x_TestFail, s
"""

#
# automagically generate the test_STD_Y_* class definitions.
#
code = ''
for d in range(0,32):
	for y in (0x20f, 0x2ff):
		for q in range(0,64,0x10):
			for v in (0xaa, 0x55):
				args = (d,y,q,v)*4
				code += template % args
exec code
