/**
 * Business Rule: Convert DOCX to PDF
 * Purpose: Converts DOCX attachments to PDF using custom API endpoint
 * Table: sys_attachment
 * When: After insert
 * Condition: Content type is DOCX
 */
(function executeRule(current, previous /*null when async*/) {
    try {
        // Configuration
        var attachmentSysId = current.sys_id;

        var apiUrl = 'https://docx-to-pdf-api-1.onrender.com/convert/docx/to/pdf';

        var tableName = 'incident';
        var tableSysId = current.table_sys_id;

        // Validate attachment exists
        var att = new GlideRecord('sys_attachment');
        if (!att.get(attachmentSysId)) {
            gs.error("[DOCX to PDF] Attachment not found with sys_id: " + attachmentSysId);
            return;
        }

        // Get file details
        var fileName = att.file_name;
        gs.info("[DOCX to PDF] Processing file: " + fileName + " | Record: " + tableName + " / " + tableSysId);

        // Configure REST request
        var r = new sn_ws.RESTMessageV2();
        r.setEndpoint(apiUrl);
        r.setHttpMethod('POST');
        r.setRequestHeader('Content-Type', 'application/octet-stream');
        r.setRequestHeader('X-Api-Client', 'ServiceNow');
        r.setRequestHeader('X-ServiceNow-Request', 'true');


        // Add request tracking
        var uuid = gs.generateGUID();
        r.setRequestHeader("Idempotency-Key", uuid);

        // Set request body from attachment
        r.setRequestBodyFromAttachment(attachmentSysId);

        // Configure response handling
        var pdfFileName = fileName.replace(/\.docx$/i, '') + '.pdf';
        r.saveResponseBodyAsAttachment(tableName, tableSysId, pdfFileName);

        // Execute request
        var response = r.execute();
        var status = response.getStatusCode();
        gs.info("[DOCX to PDF] API Response Status: " + status);

        // Process response
        if (status === 200) {
            gs.info("[DOCX to PDF] Successfully attached PDF as: " + pdfFileName);
        } else {
            gs.error("[DOCX to PDF] Conversion failed: " + response.getBody());
        }

    } catch (ex) {
        gs.error("[DOCX to PDF] Error in conversion process: " + ex.message);
    }

})(current, previous);