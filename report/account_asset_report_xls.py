# -*- encoding: utf-8 -*-

from datetime import datetime

import xlwt
from datetime import datetime
from openerp.exceptions import MissingError, ValidationError
from openerp.report import report_sxw
from openerp.addons.report_xls.report_xls import report_xls
from openerp.addons.report_xls.utils import rowcol_to_cell, _render
from openerp.tools.translate import translate, _

#FOR DEBUG - TO REMOVE
import logging
_logger = logging.getLogger(__name__)
#_logger.debug('\n\n :{}'.format(str()))


_ir_translation_name = 'account.asset.report'

class asset_report_xls_parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(asset_report_xls_parser, self).__init__(cr, uid, name, context=context)

        asset_obj = self.pool.get('account.asset.asset')
        self.context = context
        wl_acq = asset_obj._xls_acquisition_fields(cr, uid, context)
        wl_act = asset_obj._xls_active_fields(cr, uid, context)
        wl_rem = asset_obj._xls_removal_fields(cr, uid, context)
        self.localcontext.update({
            'datetime': datetime,
            'wanted_list_acquisition': wl_acq,
            'wanted_list_active': wl_act,
            'wanted_list_removal': wl_rem,
            '_': self._,
        })

    def _(self, src):
        lang = self.context.get('lang', 'en_US')
        res = translate(self.cr, _ir_translation_name, 'report', lang, src)
        return res or src

class asset_report_xls(report_xls):

    def __init__(self, name, table, rml=False, parser=False, header=True, store=False):
        super(asset_report_xls, self).__init__(name, table, rml, parser, header, store)

        # Cell Styles
        _xs = self.xls_styles
        # header

        # Report Column Headers format
        rh_cell_format = _xs['bold'] + _xs['fill'] + _xs['borders_all']
        self.rh_cell_style = xlwt.easyxf(rh_cell_format)
        self.rh_cell_style_center = xlwt.easyxf(rh_cell_format + _xs['center'])
        self.rh_cell_style_right = xlwt.easyxf(rh_cell_format + _xs['right'])

        # Type view Column format
        fill_blue = 'pattern: pattern solid, fore_color 27;'
        av_cell_format = _xs['bold'] + fill_blue + _xs['borders_all']
        self.av_cell_style = xlwt.easyxf(av_cell_format)
        self.av_cell_style_decimal = xlwt.easyxf(
            av_cell_format + _xs['right'],
            num_format_str=report_xls.decimal_format)

        # Type normal Column Data format
        an_cell_format = _xs['borders_all']
        self.an_cell_style = xlwt.easyxf(an_cell_format)
        self.an_cell_style_center = xlwt.easyxf(an_cell_format + _xs['center'])
        self.an_cell_style_date = xlwt.easyxf(
            an_cell_format + _xs['left'],
            num_format_str=report_xls.date_format)
        self.an_cell_style_decimal = xlwt.easyxf(
            an_cell_format + _xs['right'],
            num_format_str=report_xls.decimal_format)

        # totals
        rt_cell_format = _xs['bold'] + _xs['fill'] + _xs['borders_all']
        self.rt_cell_style = xlwt.easyxf(rt_cell_format)
        self.rt_cell_style_right = xlwt.easyxf(rt_cell_format + _xs['right'])
        self.rt_cell_style_decimal = xlwt.easyxf(
            rt_cell_format + _xs['right'],
            num_format_str=report_xls.decimal_format)

        # XLS Template
        self.acquisition_template = {
            'account': {
                'header':	[1, 20, 'text', _render("_('Account')")],
                'asset':	[1, 0, 'text', _render("asset.category_id.account_asset_id.code")],
                'totals':	[1, 0, 'text', _render("_('Totals')"), None, self.rt_cell_style]},
            'name': {
                'header':	[1, 40, 'text', _render("_('Name')")],
                'asset':	[1, 0, 'text', _render("asset.name or ''")],
                'totals':	[1, 0, 'text', None]},
            'code': {
                'header':	[1, 20, 'text', _render("_('Reference')")],
                'asset':	[1, 0, 'text', _render("asset.code or ''")],
                'totals':	[1, 0, 'text', None]},
            'date': {
                'header':	[1, 18, 'text', _render("_('Date')")],
                'asset':	[1, 0, 'date', _render("asset.date and datetime.strptime(asset.date,'%Y-%m-%d') or None"), None, self.an_cell_style_date],
                'totals':	[1, 0, 'text', None]},
            'value': {
                'header':	[1, 18, 'text', _render("_('Gross Value')"), None, self.rh_cell_style_right],
                'asset':	[1, 0, 'number', _render("asset.value"), None, self.an_cell_style_decimal],
                'totals':	[1, 0, 'number', None, _render("asset_total_formula"), self.rt_cell_style_decimal]},
            'salvage_value': {
                'header':	[1, 18, 'text', _render("_('Salvage Value')"), None, self.rh_cell_style_right],
                'asset':	[1, 0, 'number', _render("asset.salvage_value"), None, self.an_cell_style_decimal],
                'totals':   [1, 0, 'number', None, _render("salvage_total_formula"), self.rt_cell_style_decimal]},
        }
        

        self.active_template = {
            'account': {
                'header':	[1, 20, 'text', _render("_('Account')")],
                'asset':    [1, 0, 'text', _render("asset.category_id.account_asset_id.code")],
                'totals':   [1, 0, 'text', _render("_('Totals')"), None, self.rt_cell_style]},
            'name': {
                'header':	[1, 40, 'text', _render("_('Name')")],
                'asset':	[1, 0, 'text', _render("asset.name or ''")],
                'totals':	[1, 0, 'text', None]},
            'code': {
                'header':	[1, 20, 'text', _render("_('Reference')")],
                'asset':	[1, 0, 'text', _render("asset.code or ''")],
                'totals':	[1, 0, 'text', None]},
            'date': {
                'header':	[1, 20, 'text', _render("_('Date')")],
                'asset':    [1, 0, 'date', _render("asset.date and datetime.strptime(asset.date,'%Y-%m-%d') or None"), None, self.an_cell_style_date],
                'totals':	[1, 0, 'text', None]},
            'value': {
                'header':   [1, 18, 'text', _render("_('Gross Value')"), None, self.rh_cell_style_right],
                'asset':    [1, 0, 'number', _render("asset.asset_value"), None, self.an_cell_style_decimal],
                'totals':   [1, 0, 'number', None, _render("asset_total_formula"), self.rt_cell_style_decimal]},
            'salvage_value': {
                'header':	[1, 18, 'text', _render("_('Salvage Value')"),None, self.rh_cell_style_right],
                'asset':	[1, 0, 'number', _render("asset.salvage_value"),None, self.an_cell_style_decimal],
                'totals':	[1, 0, 'number', None, _render("salvage_total_formula"),self.rt_cell_style_decimal]},
            'fy_start_value': {
                'header':	[1, 18, 'text', _render("_('FY Start Value')"),None, self.rh_cell_style_right],
                'asset':	[1, 0, 'number', _render("asset.fy_start_value"),None, self.an_cell_style_decimal],
                'totals':	[1, 0, 'number', None, _render("fy_start_total_formula"),self.rt_cell_style_decimal]},
            'fy_depr': {
                'header':	[1, 18, 'text', _render("_('FY Depreciation')"),None, self.rh_cell_style_right],
                'asset':	[1, 0, 'number', None, _render("fy_diff_formula"),self.an_cell_style_decimal],
                'totals':	[1, 0, 'number', None, _render("fy_diff_formula"),self.rt_cell_style_decimal]},
            'fy_end_value': {
                'header':	[1, 18, 'text', _render("_('FY End Value')"),None, self.rh_cell_style_right],
                'asset':	[1, 0, 'number', _render("asset.fy_end_value"),None, self.an_cell_style_decimal],
                'totals':	[1, 0, 'number', None, _render("fy_end_total_formula"),self.rt_cell_style_decimal]},
            'fy_end_depr': {
                'header':	[1, 18, 'text', _render("_('Tot. Depreciation')"),None, self.rh_cell_style_right],
                'asset':	[1, 0, 'number', None, _render("total_depr_formula"),self.an_cell_style_decimal],
                'totals':	[1, 0, 'number', None, _render("total_depr_formula"),self.rt_cell_style_decimal]},
            'method': {
                'header':	[1, 20, 'text', _render("_('Comput. Method')"),None, self.rh_cell_style_center],
                'asset':	[1, 0, 'text', _render("asset.method or ''"),None, self.an_cell_style_center],
                'totals':	[1, 0, 'text', None]},
            'method_number': {
                'header':	[1, 20, 'text', _render("_('Number of Years')"),None, self.rh_cell_style_center],
                'asset':	[1, 0, 'number', _render("asset.method_number"),None, self.an_cell_style_center],
                'totals':	[1, 0, 'text', None]},
            'prorata': {
                'header':	[1, 20, 'text', _render("_('Prorata Temporis')"),None, self.rh_cell_style_center],
                'asset':	[1, 0, 'bool', _render("asset.prorata")],
                'totals':  	[1, 0, 'text', None]},
        }
        
        """
        self.removal_template = {
            'account': {
                'header':	[1, 20, 'text', _render("_('Account')")],
                'asset':	[1, 0, 'text',_render("asset.category_id.account_asset_id.code")],
                'totals':	[1, 0, 'text', _render("_('Totals')"),None, self.rt_cell_style]},
            'name': {
                'header':   [1, 40, 'text', _render("_('Name')")],
                'asset':	[1, 0, 'text', _render("asset.name or ''")],
                'totals':	[1, 0, 'text', None]},
            'code': {
                'header':	[1, 20, 'text', _render("_('Reference')")],
                'asset':	[1, 0, 'text', _render("asset.code or ''")],
                'totals':	[1, 0, 'text', None]},
            'date_remove': {
                'header':	[1, 20, 'text', _render("_('Asset Removal Date')")],
                'asset':	[1, 0, 'date',_render("asset.date_remove and datetime.strptime(asset.date_remove,'%Y-%m-%d') or None"), None, self.an_cell_style_date],
                'totals':	[1, 0, 'text', None]},
            'asset_value': {
                'header':	[1, 18, 'text', _render("_('Asset Value')"),None, self.rh_cell_style_right],
                'asset':	[1, 0, 'number', _render("asset.asset_value"),None, self.an_cell_style_decimal],
                'totals':	[1, 0, 'number', None, _render("asset_total_formula"), self.rt_cell_style_decimal]},
            'salvage_value': {
                'header':	[1, 18, 'text', _render("_('Salvage Value')"),None, self.rh_cell_style_right],
                'asset':	[1, 0, 'number', _render("asset.salvage_value"),None, self.an_cell_style_decimal],
                'totals':	[1, 0, 'number', None, _render("salvage_total_formula"), self.rt_cell_style_decimal]},
        }
        """

    def _get_title(self, report, format='normal'):
        
        report_title_normal_dict = {'acquisition':'New Acquisitions',
                             'active':'Active Assets',
                             'normal':'Removed Assets'}
        report_title_short_dict = {'acquisition':'ACQ',
                             'active':'ACT',
                             'normal':'DSP'}
        
        year_string = datetime.strptime(self.date_start, "%Y-%m-%d").date().strftime("%y")
        
        if format == 'normal':
            return 'Fiscal Year {} : {}'.format(year_string, report_title_normal_dict[report])
        elif format == 'short':
            return '{}-{}'.format(year_string, report_title_short_dict[report])

    def _report_title(self, ws, _p, row_pos, _xs, title):
        cell_style = xlwt.easyxf(_xs['xls_title'])
        c_specs = [('report_name', 1, 0, 'text', title),]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=cell_style)
        return row_pos + 1

    def _empty_report(self, ws, _p, row_pos, _xs, report):
        cell_style = xlwt.easyxf(_xs['bold'])

        if report == 'acquisition':
            suffix = _('New Acquisitions')
        elif report == 'active':
            suffix = _('Active Assets')
        else:
            suffix = _('Removed Assets')
        no_entries = _("No") + " " + suffix
        c_specs = [('ne', 1, 0, 'text', no_entries),]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=cell_style)

    def _acquisition_report(self, _p, _xs, data, objects, wb):
        cr = self.cr
        uid = self.uid
        wl_acq = _p.wanted_list_acquisition
        template = self.acquisition_template
        asset_obj = self.pool.get('account.asset.asset')
        
        #Create new sheet and set title
        title = self._get_title('acquisition', 'normal')
        title_short = self._get_title('acquisition', 'short')
        sheet_name = title_short[:31].replace('/', '-')
        ws = wb.add_sheet(sheet_name)
        
        #Sheet options
        ws.panes_frozen = True
        ws.remove_splits = True
        ws.portrait = 0  # Landscape
        ws.fit_width_to_pages = 1
        row_pos = 0
        
        #Set print header/footer
        ws.header_str = self.xls_headers['standard']
        ws.footer_str = self.xls_footers['standard']
        row_pos = self._report_title(ws, _p, row_pos, _xs, title)
        
        #Search data for report
        asset_ids = asset_obj.search(cr, uid, [('company_id', '=', self.company_id),('date','>=',self.date_start),('date','<=',self.date_end)],order='date')

        #Empty report
        if not asset_ids or len(asset_ids)==0:
            return self._empty_report(ws, _p, row_pos, _xs, 'acquisition')
        
        #Set header
        c_specs = map(lambda x: self.render(x, template, 'header', render_space={'_': _p._}), wl_acq)
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=self.rh_cell_style, set_column_size=True)
        ws.set_horz_split_pos(row_pos)
        row_pos_start = row_pos
        
        #Check if account exists
        if 'account' not in wl_acq:
            raise MissingError(_("The 'account' field is a mandatory entry of the '_xls_acquisition_fields' list !"))
        
        #Set asset
        for asset in asset_obj.browse(cr, uid, asset_ids):          
            c_specs = map( lambda x: self.render(x, template, 'asset'), wl_acq)
            row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
            row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=self.an_cell_style)
                
        #Set totals
        value_pos = 'value' in wl_acq and wl_acq.index('value')
        salvage_value_pos = 'salvage_value' in wl_acq and wl_acq.index('salvage_value')
        asset_number = len(asset_ids)
        
        #---------Format excel SUM string. ex: SUM(E4:E22)
        asset_total_formula = 'SUM({}:{})'.format(rowcol_to_cell(row_pos_start, value_pos),rowcol_to_cell(row_pos_start+asset_number-1, value_pos))
        salvage_total_formula = 'SUM({}:{})'.format(rowcol_to_cell(row_pos_start, salvage_value_pos),rowcol_to_cell(row_pos_start+asset_number-1, salvage_value_pos))

        #---------Render totals
        c_specs = map(lambda x: self.render(x, template, 'totals'), wl_acq)
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=self.rt_cell_style_right)
    
    def _active_report(self, _p, _xs, data, objects, wb):
        cr = self.cr
        uid = self.uid
        wl_acq = _p.wanted_list_acquisition
        template = self.acquisition_template
        asset_obj = self.pool.get('account.asset.asset')
        depreciation_line_obj = self.pool.get('account.asset.depreciation.line')

        #Create new sheet and set title
        title = self._get_title('active', 'normal')
        title_short = self._get_title('active', 'short')
        sheet_name = title_short[:31].replace('/', '-')
        ws = wb.add_sheet(sheet_name)
        
        #Sheet options
        ws.panes_frozen = True
        ws.remove_splits = True
        ws.portrait = 0  # Landscape
        ws.fit_width_to_pages = 1
        row_pos = 0
        
        #Set print header/footer
        ws.header_str = self.xls_headers['standard']
        ws.footer_str = self.xls_footers['standard']
        row_pos = self._report_title(ws, _p, row_pos, _xs, title)
        
        #Search data for report
        asset_ids = asset_obj.search(cr, uid, [('company_id', '=', self.company_id),('state','=','open'),('date','<=',self.date_end)],order='date')

        #Empty report
        if not asset_ids or len(asset_ids)==0:
            return self._empty_report(ws, _p, row_pos, _xs, 'active')
        
        #Set header
        c_specs = map(lambda x: self.render(x, template, 'header', render_space={'_': _p._}), wl_acq)
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=self.rh_cell_style, set_column_size=True)
        ws.set_horz_split_pos(row_pos)
        row_pos_start = row_pos
        
        #Check if account exists
        if 'account' not in wl_acq:
            raise MissingError(_("The 'account' field is a mandatory entry of the '_xls_acquisition_fields' list !"))
        
        #Set asset
        for asset in asset_obj.browse(cr, uid, asset_ids):          
            c_specs = map( lambda x: self.render(x, template, 'asset'), wl_acq)
            row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
            row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=self.an_cell_style)
                
        #Set totals
        value_pos = 'value' in wl_acq and wl_acq.index('value')
        salvage_value_pos = 'salvage_value' in wl_acq and wl_acq.index('salvage_value')
        asset_number = len(asset_ids)
        
        #---------Format excel SUM string. ex: SUM(E4:E22)
        asset_total_formula = 'SUM({}:{})'.format(rowcol_to_cell(row_pos_start, value_pos),rowcol_to_cell(row_pos_start+asset_number-1, value_pos))
        salvage_total_formula = 'SUM({}:{})'.format(rowcol_to_cell(row_pos_start, salvage_value_pos),rowcol_to_cell(row_pos_start+asset_number-1, salvage_value_pos))

        #---------Render totals
        c_specs = map(lambda x: self.render(x, template, 'totals'), wl_acq)
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=self.rt_cell_style_right)
        """
        cr = self.cr
        uid = self.uid
        context = self.context
        wl_act = _p.wanted_list_active
        template = self.active_template
        asset_obj = self.pool.get('account.asset.asset')

        title = self._get_title('active', 'normal')
        title_short = self._get_title('active', 'short')
        sheet_name = title_short[:31].replace('/', '-')
        ws = wb.add_sheet(sheet_name)
        ws.panes_frozen = True
        ws.remove_splits = True
        ws.portrait = 0  # Landscape
        ws.fit_width_to_pages = 1
        row_pos = 0
        ws.header_str = self.xls_headers['standard']
        ws.footer_str = self.xls_footers['standard']
        row_pos = self._report_title(ws, _p, row_pos, _xs, title)

        cr.execute(
            "SELECT id FROM account_asset_asset "
            "WHERE date_start <= %s"
            "AND ((date_remove IS NULL) OR "
            "(date_remove >= %s AND date_remove <= %s)) "
            "AND id IN %s AND type = 'normal' "
            "ORDER BY date_start ASC",
            (fy.date_stop, fy.date_start, fy.date_stop, tuple(self.asset_ids))
            )
        act_ids = [x[0] for x in cr.fetchall()]

        if not act_ids:
            return self._empty_report(ws, _p, row_pos, _xs, 'active')

        c_specs = map(
            lambda x: self.render(
                x, template, 'header',
                render_space={'_': _p._}),
            wl_act)
        row_data = self.xls_row_template(
            c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=self.rh_cell_style,
            set_column_size=True)
        ws.set_horz_split_pos(row_pos)

        row_pos_start = row_pos
        if 'account' not in wl_act:
            raise MissingError(_('Customization Error'), _(
                "The 'account' field is a mandatory entry of the "
                "'_xls_active_fields' list !"))
        asset_value_pos = 'asset_value' in wl_act and \
            wl_act.index('asset_value')
        salvage_value_pos = 'salvage_value' in wl_act and \
            wl_act.index('salvage_value')
        fy_start_value_pos = 'fy_start_value' in wl_act and \
            wl_act.index('fy_start_value')
        fy_end_value_pos = 'fy_end_value' in wl_act and \
            wl_act.index('fy_end_value')

        acts = filter(lambda x: x[0] in act_ids, self.assets)
        acts_and_parents = []

        entries = []
        for asset_i, data in enumerate(acts_and_parents):
            entry = {}
            asset = asset_obj.browse(cr, uid, data[0], context=context)

            if data[1] == 'view':
                cp_i = asset_i + 1
                cp = []
                for a in acts_and_parents[cp_i:]:
                    if a[2] == data[0]:
                        cp.append(cp_i)
                    cp_i += 1
                entry['child_pos'] = cp

            else:

                # fy_start_value
                cr.execute(
                    "SELECT depreciated_value "
                    "FROM account_asset_depreciation_line "
                    "WHERE line_date >= %s"
                    "AND asset_id = %s AND type = 'depreciate' "
                    "ORDER BY line_date ASC LIMIT 1",
                    (fy.date_start, data[0]))
                res = cr.fetchone()
                if res:
                    value_depreciated = res[0]
                elif asset.state in ['close', 'removed']:
                    value_depreciated = asset.value_depreciated
                elif not asset.method_number:
                    value_depreciated = 0.0
                else:
                    error_name = asset.name
                    if asset.code:
                        error_name += ' (' + asset.code + ')' or ''
                    if asset.state in ['open']:
                        cr.execute(
                            "SELECT line_date "
                            "FROM account_asset_depreciation_line "
                            "WHERE asset_id = %s AND type = 'depreciate' "
                            "AND init_entry=FALSE AND move_check=FALSE "
                            "AND line_date < %s"
                            "ORDER BY line_date ASC LIMIT 1",
                            (data[0], fy.date_start))
                        res = cr.fetchone()
                        if res:
                            raise ValidationError(_("You can not report on a Fiscal Year with unposted entries in prior years. Please post depreciation table entry dd. '%s'  of asset '%s' !") % (res[0], error_name))
                        else:
                            raise ValidationError(_("Depreciation Table error for asset %s !") % error_name)
                    else:
                        raise ValidationError(_("Depreciation Table error for asset %s !") % error_name)
                asset.fy_start_value = asset.asset_value - value_depreciated

                # fy_end_value
                cr.execute(
                    "SELECT depreciated_value "
                    "FROM account_asset_depreciation_line "
                    "WHERE line_date > %s"
                    "AND asset_id = %s AND type = 'depreciate' "
                    "ORDER BY line_date ASC LIMIT 1",
                    (fy.date_stop, data[0]))
                res = cr.fetchone()
                if res:
                    value_depreciated = res[0]
                elif not asset.method_number:
                    value_depreciated = 0.0
                else:
                    value_depreciated = asset.asset_value
                asset.fy_end_value = asset.asset_value - value_depreciated
            entry['asset'] = asset
            entries.append(entry)

        for entry in entries:
            asset = entry['asset']

            fy_start_value_cell = rowcol_to_cell(row_pos, fy_start_value_pos)
            fy_end_value_cell = rowcol_to_cell(row_pos, fy_end_value_pos)
            asset_value_cell = rowcol_to_cell(row_pos, asset_value_pos)
            fy_diff_formula = fy_start_value_cell + '-' + fy_end_value_cell
            total_depr_formula = asset_value_cell + '-' + fy_end_value_cell

            if asset.type == 'view':

                asset_value_cells = [
                    rowcol_to_cell(row_pos_start + x, asset_value_pos)
                    for x in entry['child_pos']]
                asset_formula = '+'.join(asset_value_cells)  # noqa: disable F841, report_xls namespace trick

                salvage_value_cells = [
                    rowcol_to_cell(row_pos_start + x, salvage_value_pos)
                    for x in entry['child_pos']]
                salvage_formula = '+'.join(salvage_value_cells)  # noqa: disable F841, report_xls namespace trick

                fy_start_value_cells = [
                    rowcol_to_cell(row_pos_start + x, fy_start_value_pos)
                    for x in entry['child_pos']]
                fy_start_formula = '+'.join(fy_start_value_cells)  # noqa: disable F841, report_xls namespace trick

                fy_end_value_cells = [
                    rowcol_to_cell(row_pos_start + x, fy_end_value_pos)
                    for x in entry['child_pos']]
                fy_end_formula = '+'.join(fy_end_value_cells)  # noqa: disable F841, report_xls namespace trick

                c_specs = map(
                    lambda x: self.render(
                        x, template, 'asset_view'),
                    wl_act)
                row_data = self.xls_row_template(
                    c_specs, [x[0] for x in c_specs])
                row_pos = self.xls_write_row(
                    ws, row_pos, row_data, row_style=self.av_cell_style)

            else:
                c_specs = map(
                    lambda x: self.render(
                        x, template, 'asset'),
                    wl_act)
                row_data = self.xls_row_template(
                    c_specs, [x[0] for x in c_specs])
                row_pos = self.xls_write_row(
                    ws, row_pos, row_data, row_style=self.an_cell_style)

        asset_total_formula = rowcol_to_cell(row_pos_start, asset_value_pos)  # noqa: disable F841, report_xls namespace trick
        salvage_total_formula = rowcol_to_cell(row_pos_start,  # noqa: disable F841, report_xls namespace trick
                                               salvage_value_pos)
        fy_start_total_formula = rowcol_to_cell(row_pos_start,  # noqa: disable F841, report_xls namespace trick
                                                fy_start_value_pos)
        fy_end_total_formula = rowcol_to_cell(row_pos_start, fy_end_value_pos)  # noqa: disable F841, report_xls namespace trick

        fy_start_value_cell = rowcol_to_cell(row_pos, fy_start_value_pos)
        fy_end_value_cell = rowcol_to_cell(row_pos, fy_end_value_pos)
        asset_value_cell = rowcol_to_cell(row_pos, asset_value_pos)
        fy_diff_formula = fy_start_value_cell + '-' + fy_end_value_cell  # noqa: disable F841, report_xls namespace trick
        total_depr_formula = asset_value_cell + '-' + fy_end_value_cell  # noqa: disable F841, report_xls namespace trick

        c_specs = map(
            lambda x: self.render(
                x, template, 'totals'),
            wl_act)
        row_data = self.xls_row_template(
            c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=self.rt_cell_style_right)
        """
    def _removal_report(self, _p, _xs, data, objects, wb):
        cr = self.cr
        uid = self.uid
        context = self.context
        wl_dsp = _p.wanted_list_removal
        template = self.removal_template
        asset_obj = self.pool.get('account.asset.asset')

        title = self._get_title('removal', 'normal')
        title_short = self._get_title('removal', 'short')
        sheet_name = title_short[:31].replace('/', '-')
        ws = wb.add_sheet(sheet_name)
        ws.panes_frozen = True
        ws.remove_splits = True
        ws.portrait = 0  # Landscape
        ws.fit_width_to_pages = 1
        row_pos = 0
        ws.header_str = self.xls_headers['standard']
        ws.footer_str = self.xls_footers['standard']
        row_pos = self._report_title(ws, _p, row_pos, _xs, title)

        cr.execute(
            "SELECT id FROM account_asset_asset "
            "WHERE date_remove >= %s AND date_remove <= %s"
            "AND id IN %s AND type = 'normal' "
            "ORDER BY date_remove ASC",
            (fy.date_start, fy.date_stop, tuple(self.asset_ids)))
        dsp_ids = [x[0] for x in cr.fetchall()]

        if not dsp_ids:
            return self._empty_report(ws, _p, row_pos, _xs, 'removal')

        c_specs = map(
            lambda x: self.render(
                x, template, 'header',
                render_space={'_': _p._}),
            wl_dsp)
        row_data = self.xls_row_template(
            c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=self.rh_cell_style,
            set_column_size=True)
        ws.set_horz_split_pos(row_pos)

        row_pos_start = row_pos
        if 'account' not in wl_dsp:
            raise MissingError(_("The 'account' field is a mandatory entry of the '_xls_removal_fields' list !"))
        asset_value_pos = 'asset_value' in wl_dsp and \
            wl_dsp.index('asset_value')
        salvage_value_pos = 'salvage_value' in wl_dsp and \
            wl_dsp.index('salvage_value')

        dsps = filter(lambda x: x[0] in dsp_ids, self.assets)
        dsps_and_parents = []

        entries = []
        for asset_i, data in enumerate(dsps_and_parents):
            entry = {}
            asset = asset_obj.browse(cr, uid, data[0], context=context)
            if data[1] == 'view':
                cp_i = asset_i + 1
                cp = []
                for a in dsps_and_parents[cp_i:]:
                    if a[2] == data[0]:
                        cp.append(cp_i)
                    cp_i += 1
                entry['child_pos'] = cp
            entry['asset'] = asset
            entries.append(entry)

        for entry in entries:
            asset = entry['asset']
            if asset.type == 'view':
                asset_value_cells = [
                    rowcol_to_cell(row_pos_start + x, asset_value_pos)
                    for x in entry['child_pos']]
                asset_formula = '+'.join(asset_value_cells)  # noqa: disable F841, report_xls namespace trick
                salvage_value_cells = [rowcol_to_cell(row_pos_start + x, salvage_value_pos) for x in entry['child_pos']]
                salvage_formula = '+'.join(salvage_value_cells)  # noqa: disable F841, report_xls namespace trick
                c_specs = map(
                    lambda x: self.render(
                        x, template, 'asset_view'),
                    wl_dsp)
                row_data = self.xls_row_template(
                    c_specs, [x[0] for x in c_specs])
                row_pos = self.xls_write_row(
                    ws, row_pos, row_data, row_style=self.av_cell_style)
            else:
                c_specs = map(
                    lambda x: self.render(
                        x, template, 'asset'),
                    wl_dsp)
                row_data = self.xls_row_template(
                    c_specs, [x[0] for x in c_specs])
                row_pos = self.xls_write_row(
                    ws, row_pos, row_data, row_style=self.an_cell_style)

        asset_total_formula = rowcol_to_cell(row_pos_start, asset_value_pos)  # noqa: disable F841, report_xls namespace trick
        salvage_total_formula = rowcol_to_cell(row_pos_start,   # noqa: disable F841, report_xls namespace trick
                                               salvage_value_pos)

        c_specs = map(
            lambda x: self.render(
                x, template, 'totals'),
            wl_dsp)
        row_data = self.xls_row_template(
            c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=self.rt_cell_style_right)

    def generate_xls_report(self, _p, _xs, data, objects, wb):
        wl_act = _p.wanted_list_active  # noqa: disable F841, report_xls namespace trick
        wl_rem = _p.wanted_list_removal  # noqa: disable F841, report_xls namespace trick
        self.date_start = data['date_start']
        self.date_end = data['date_end']
        self.company_id = data['company_id']

        self._acquisition_report(_p, _xs, data, objects, wb)
        #self._active_report(_p, _xs, data, objects, wb)
        #self._removal_report(_p, _xs, data, objects, wb)

asset_report_xls('report.account.asset.xls', 'account.asset.asset', parser=asset_report_xls_parser)
