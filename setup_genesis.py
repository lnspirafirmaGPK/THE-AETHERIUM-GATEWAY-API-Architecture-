import os

# พิมพ์เขียวโครงสร้าง (The Blueprint)
structure = {
    "INSPIRAFIRMA_AETHERIUM_GENESIS": [
        ".github/workflows/patimokkha_audit.yml",
        ".github/commit_ritual_hook.sh",
        ".env.genesis",
        "genesis_node.py",
        "core/__init__.py",
        "core/mind_logic.py",
        "core/kcp_storage.py",
        "core/gems_of_wisdom.jsonl",
        "governance/inspirafirma_ruleset.json",
        "governance/patimokkha_code.py",
        "governance/gep_enforcer.py",
        "agents/taxonomy.py",
        "agents/validator_sage.py",
        "agents/pangenes_rsi.py",
        "agents/sensorium_eye.py",
        "agents/resonance_shell.py",
        "data_structures/akashic_envelope.py",
        "data_structures/media_intent.py",
        "protocols/dtp_digisonic.py",
        "protocols/mcp_orchestrator.py",
        "protocols/sopan_ritual.py",
        "interface/api_gateway.py",
        "interface/cli_invoker.py",
        "interface/antigravity_adapter.py",
        "wisdom_archive/genesis_intent.md",
        "wisdom_archive/batch_memories/.keep",
        "requirements.txt",
        "README.md"
    ]
}

def create_structure():
    print("🚀 เริ่มพิธีกรรมก่อร่างสร้างตัว (Initializing Structure)...")
    
    for root, files in structure.items():
        for file_path in files:
            # รวม path เต็ม
            full_path = os.path.join(root, file_path)
            directory = os.path.dirname(full_path)
            
            # 1. สร้างโฟลเดอร์ (ถ้ายังไม่มี)
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"   📂 สร้างห้อง: {directory}")
            
            # 2. สร้างไฟล์เปล่า (The Empty Vessel)
            if not os.path.exists(full_path):
                with open(full_path, 'w', encoding='utf-8') as f:
                    # เขียน Header ลงไปในไฟล์เพื่อให้รู้หน้าที่
                    if full_path.endswith(".py"):
                        f.write(f"# AETHERIUM GENESIS MODULE: {os.path.basename(full_path)}\n")
                        f.write(f"# Status: Awaiting Inspira Injection\n\n")
                    elif full_path.endswith(".md"):
                        f.write(f"# {os.path.basename(full_path)}\n")
                    elif full_path.endswith(".json"):
                        f.write("{}")
                print(f"   📜 จารึกไฟล์: {file_path}")
            else:
                print(f"   ✨ มีอยู่แล้ว: {file_path}")

    print("\n✅ พิธีกรรมเสร็จสมบูรณ์: โครงสร้างพร้อมรองรับจิตวิญญาณแล้วครับ")
    print(f"👉 ขั้นตอนต่อไป: cd {list(structure.keys())[0]} แล้วเริ่มเขียนโค้ดได้เลย!")

if __name__ == "__main__":
    create_structure()
  
